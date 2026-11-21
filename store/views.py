"""JSON endpoints for the storefront and the coffee wizard.

These return the same shapes the React components already expect, so the
frontend only had to swap hard-coded modules for a fetch.
"""

import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .models import (
    BrewMethod,
    ConsumptionTier,
    Origin,
    Product,
    RatingLevel,
    TasteProfile,
    WizardSubmission,
)


# ── Serializers ────────────────────────────────────────────────────────────


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "type": product.type_label,
        "weight": product.weight or "—",
        # The card formats the number itself, so send raw toman (or None).
        "price": product.price,
        "grade": product.grade_display,
        "gradeType": product.grade,
        "image": product.image,
    }


def serialize_method(method: BrewMethod) -> dict:
    return {
        "id": method.id,
        "name": method.name,
        "slug": method.slug,
        "image": method.image,
        "order": method.order,
        "description": method.description,
    }


def serialize_origin(origin: Origin) -> dict:
    return {
        "id": origin.id,
        "name": origin.name,
        "slug": origin.slug,
        "image": origin.image,
        "flag": origin.flag,
        "tasting": origin.tasting,
        "order": origin.order,
        "acidity": origin.acidity,
        "acidity_display": origin.acidity_display,
        "body": origin.body,
        "body_display": origin.body_display,
        "sweetness": origin.sweetness,
        "sweetness_display": origin.sweetness_display,
        "aroma": origin.aroma,
        "aroma_display": origin.aroma_display,
        "bitterness": origin.bitterness,
        "bitterness_display": origin.bitterness_display,
    }


def serialize_taste(taste: TasteProfile) -> dict:
    return {
        "id": taste.id,
        "name": taste.name,
        "slug": taste.slug,
        "image": taste.image,
        "rating": taste.rating,
    }


def serialize_consumption(tier: ConsumptionTier) -> dict:
    return {
        "id": tier.id,
        "label": tier.label,
        "range": tier.grams_range,
        "hint": tier.hint,
        "image": tier.image,
        "rating": tier.rating,
    }


# ── Storefront ─────────────────────────────────────────────────────────────


@require_GET
def product_list(request):
    """All active products, optionally filtered by `?bestseller=1`."""
    products = Product.objects.filter(is_active=True)

    if request.GET.get("bestseller") in {"1", "true", "True"}:
        products = products.filter(is_bestseller=True)

    return JsonResponse({"products": [serialize_product(p) for p in products]})


@require_GET
def bestsellers(request):
    """Dedicated shelf endpoint so the homepage can stay declarative."""
    products = Product.objects.filter(is_active=True, is_bestseller=True)
    return JsonResponse({"products": [serialize_product(p) for p in products]})


@require_GET
def product_detail(request, slug: str):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return JsonResponse({"product": serialize_product(product)})


# ── Wizard options ─────────────────────────────────────────────────────────


@require_GET
def brew_method_list(request):
    return JsonResponse({"methods": [serialize_method(m) for m in BrewMethod.objects.all()]})


@require_GET
def origin_list(request):
    return JsonResponse({"origins": [serialize_origin(o) for o in Origin.objects.all()]})


@require_GET
def taste_list(request):
    return JsonResponse({"tastes": [serialize_taste(t) for t in TasteProfile.objects.all()]})


@require_GET
def consumption_list(request):
    return JsonResponse(
        {"consumption": [serialize_consumption(c) for c in ConsumptionTier.objects.all()]}
    )


@require_GET
def wizard_options(request):
    """One round-trip payload for every wizard carousel."""
    return JsonResponse(
        {
            "methods": [serialize_method(m) for m in BrewMethod.objects.all()],
            "origins": [serialize_origin(o) for o in Origin.objects.all()],
            "tastes": [serialize_taste(t) for t in TasteProfile.objects.all()],
            "consumption": [serialize_consumption(c) for c in ConsumptionTier.objects.all()],
        }
    )


# ── Recommendation ─────────────────────────────────────────────────────────

# How strongly each taste direction pulls the recommender toward acidity.
_TASTE_ACIDITY_BIAS = {
    "fruity": -1,  # fruity -> wants high acidity
    "floral": -1,
    "chocolate": 1,  # chocolatey -> prefers lower acidity
    "nutty": 1,
    "mild": 1,
    "strong": 0,
}

_LEVEL_SCORE = {
    RatingLevel.LOW: 1,
    RatingLevel.MEDIUM: 2,
    RatingLevel.GOOD: 3,
    RatingLevel.HIGH: 4,
}


def _score_origin(origin: Origin, *, wants_acidity: bool, robusta_ratio: int) -> int:
    """Higher is better.

    Robusta-heavy blends pair with low-acidity origins, while arabica-forward
    blends suit bright, acidic ones; body tracks the robusta share.
    """
    acid = _LEVEL_SCORE[origin.acidity]
    body = _LEVEL_SCORE[origin.body]
    score = 0

    if wants_acidity:
        score += acid * 2
    else:
        score += (5 - acid) * 2

    # Heavier robusta share wants more body.
    score += body if robusta_ratio >= 50 else (5 - body)

    return score


# Anonymous JSON endpoint called from the browser; it carries no session
# credentials, so CSRF protection adds nothing here.
@csrf_exempt
@require_POST
def recommend(request):
    """Turn wizard answers into a ranked shortlist plus a blend summary."""
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "بدنه‌ی درخواست باید JSON باشد."}, status=400)

    try:
        robusta = int(payload.get("robusta", 50))
    except (TypeError, ValueError):
        return JsonResponse({"error": "robusta باید عدد باشد."}, status=400)

    robusta = max(0, min(100, robusta))
    arabica = 100 - robusta

    taste_slug = payload.get("taste_slug")
    method_slug = payload.get("method_slug")
    consumption_id = payload.get("consumption_id")

    taste = TasteProfile.objects.filter(slug=taste_slug).first() if taste_slug else None
    method = BrewMethod.objects.filter(slug=method_slug).first() if method_slug else None
    try:
        consumption = (
            ConsumptionTier.objects.filter(id=consumption_id).first()
            if consumption_id
            else None
        )
    except (TypeError, ValueError):
        consumption = None

    wants_acidity = robusta < 50
    if taste is not None and taste.slug in _TASTE_ACIDITY_BIAS:
        wants_acidity = _TASTE_ACIDITY_BIAS[taste.slug] < 0

    ranked = sorted(
        Origin.objects.all(),
        key=lambda origin: _score_origin(
            origin, wants_acidity=wants_acidity, robusta_ratio=robusta
        ),
        reverse=True,
    )

    top_origin = ranked[0] if ranked else None
    WizardSubmission.objects.create(
        method=method,
        taste=taste,
        consumption=consumption,
        robusta=robusta,
        recommended_origin=top_origin,
    )

    return JsonResponse(
        {
            "blend": {
                "robusta": robusta,
                "arabica": arabica,
                "label": (
                    "ترکیب متعادل"
                    if robusta == 50
                    else ("غالب روبوستا" if robusta > 50 else "غالب عربیکا")
                ),
            },
            "method": serialize_method(method) if method else None,
            "taste": serialize_taste(taste) if taste else None,
            "consumption": serialize_consumption(consumption) if consumption else None,
            "origins": [serialize_origin(o) for o in ranked[:3]],
        }
    )


@ensure_csrf_cookie
@require_GET
def csrf_token(request):
    """Lets the frontend obtain a CSRF cookie before POSTing."""
    return JsonResponse({"ok": True})
