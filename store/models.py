"""Catalog models backing the storefront and the coffee wizard.

Everything the frontend renders — product cards, brew methods, origins, taste
profiles, consumption tiers — lives here so content is editable in the Django
admin instead of being hard-coded in React.
"""

from django.db import models


class RatingLevel(models.TextChoices):
    """Flavour intensity used by origins and taste profiles."""

    LOW = "low", "کم"
    MEDIUM = "medium", "متوسط"
    GOOD = "good", "خوب"
    HIGH = "high", "زیاد"


class BrewMethod(models.Model):
    """A device the customer brews with, e.g. V60 or a moka pot."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    image = models.CharField(
        max_length=200,
        help_text="Path relative to the frontend public dir, e.g. /media/brew_methods/v60.png",
    )
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Origin(models.Model):
    """A single-origin coffee source country."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    image = models.CharField(max_length=200)
    flag = models.CharField(max_length=200, blank=True)
    tasting = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short tasting note; may contain a newline.",
    )
    order = models.PositiveIntegerField(default=0)

    acidity = models.CharField(max_length=8, choices=RatingLevel.choices, default=RatingLevel.MEDIUM)
    body = models.CharField(max_length=8, choices=RatingLevel.choices, default=RatingLevel.MEDIUM)
    sweetness = models.CharField(max_length=8, choices=RatingLevel.choices, default=RatingLevel.MEDIUM)
    aroma = models.CharField(max_length=8, choices=RatingLevel.choices, default=RatingLevel.MEDIUM)
    bitterness = models.CharField(max_length=8, choices=RatingLevel.choices, default=RatingLevel.MEDIUM)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    def _display(self, field: str) -> str:
        return RatingLevel(self.serializable_value(field)).label

    # The frontend expects both the raw level and its Persian label; exposing
    # them as properties keeps the serializer trivial and the API stable.
    @property
    def acidity_display(self):
        return self._display("acidity")

    @property
    def body_display(self):
        return self._display("body")

    @property
    def sweetness_display(self):
        return self._display("sweetness")

    @property
    def aroma_display(self):
        return self._display("aroma")

    @property
    def bitterness_display(self):
        return self._display("bitterness")


class TasteProfile(models.Model):
    """A flavour direction offered in the wizard (fruity, chocolatey, …)."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    image = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ConsumptionTier(models.Model):
    """How much coffee the customer drinks, used to size the recommendation."""

    label = models.CharField(max_length=40)
    grams_range = models.CharField(max_length=40, help_text="e.g. 125 - 250 گرم")
    hint = models.CharField(max_length=80, blank=True)
    image = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class WizardSubmission(models.Model):
    """One completed run of the coffee wizard, kept for the dashboard."""

    method = models.ForeignKey(BrewMethod, null=True, blank=True, on_delete=models.SET_NULL)
    taste = models.ForeignKey(TasteProfile, null=True, blank=True, on_delete=models.SET_NULL)
    consumption = models.ForeignKey(
        ConsumptionTier, null=True, blank=True, on_delete=models.SET_NULL
    )
    robusta = models.PositiveSmallIntegerField(default=50)
    recommended_origin = models.ForeignKey(
        Origin, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"wizard run #{self.pk} ({self.robusta}% robusta)"


class Product(models.Model):
    """A coffee SKU shown in the storefront shelves."""

    class Grade(models.TextChoices):
        NIK = "nik", "نیک"
        MOTEVAST = "motevaset", "متوسط"

    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    type_label = models.CharField(max_length=40, help_text="e.g. دانه / اسپرسو")
    weight = models.CharField(max_length=40, blank=True)

    # Prices are stored in toman as integers. Blank/null means "coming soon",
    # which the card renders as «به‌زودی» instead of a number.
    price = models.PositiveIntegerField(null=True, blank=True)

    grade = models.CharField(max_length=10, choices=Grade.choices, default=Grade.NIK)
    image = models.CharField(
        max_length=20,
        default="☕",
        help_text="Emoji shown in the card badge.",
    )

    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def grade_display(self):
        return self.Grade(self.grade).label
