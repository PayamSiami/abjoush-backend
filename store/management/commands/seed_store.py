"""Seed the store catalog with the data the storefront used to hard-code.

Idempotent: run it as often as you like, rows are updated in place.
    python manage.py seed_store
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import (
    BrewMethod,
    ConsumptionTier,
    Origin,
    Product,
    RatingLevel,
    TasteProfile,
)

BREW_METHODS = [
    ("V60", "v60", "v60.png", "دم‌آوری قطره‌ای کلاسیک.", 0),
    ("اسپرسو خانگی", "home-espresso", "espresso-home.png", "اسپرسوی غلیظ خانگی.", 1),
    ("ایروپرس", "aeropress", "aeropress.png", "دم‌آوری با فشار هوا، همه‌کاره.", 2),
    ("سایفون", "siphon", "siphon.png", "دم‌آوری با فشار خلأ و نمایشی.", 3),
    ("فرانسه ساز", "france-press", "france-press.png", "بدنه‌ی کامل و بافت غنی.", 4),
    ("فرنچ پرس", "french-press", "french-press.png", "بدنه‌ی کامل و بافت غنی.", 5),
    ("کلد برو", "cold-brew", "cold-brew.png", "دم‌آوری سرد و ملایم.", 6),
    ("کمکس", "chemex", "chemex.png", "شفاف و تمیز، مناسب عربیکای روشن.", 7),
    ("موکاپات قهوه", "moka-pot", "moka-pot.png", "قهوه‌ی غلیظ روی گاز.", 8),
    ("نانو پرسو", "nano-espresso", "nano-espresso.png", "اسپرسوی حرفه‌ای کافه‌ای.", 9),
    ("نیمه صنعتی", "semi-industrial", "semi-industrial.png", "دستگاه نیمه‌صنعتی پرقدرت.", 10),
]

ORIGINS = [
    {
        "name": "برزیل",
        "slug": "brazil",
        "image": "/media/origins/brazil.png",
        "flag": "/media/flags/brazil.png",
        "tasting": "میوه‌ای، اسیدی\nو پرحسم",
        "order": 0,
        "acidity": RatingLevel.HIGH,
        "body": RatingLevel.LOW,
        "sweetness": RatingLevel.GOOD,
        "aroma": RatingLevel.HIGH,
        "bitterness": RatingLevel.LOW,
    },
    {
        "name": "کلمبیا",
        "slug": "colombia",
        "image": "/media/origins/colombia.jpg",
        "flag": "/media/flags/colombia.png",
        "tasting": "معتدل، شکلاتی\nو شیرین",
        "order": 1,
        "acidity": RatingLevel.MEDIUM,
        "body": RatingLevel.GOOD,
        "sweetness": RatingLevel.GOOD,
        "aroma": RatingLevel.MEDIUM,
        "bitterness": RatingLevel.MEDIUM,
    },
    {
        "name": "پرو",
        "slug": "peru",
        "image": "/media/origins/peru.jpg",
        "flag": "/media/flags/peru.png",
        "tasting": "ملایم، آجیلی\nو متعادل",
        "order": 2,
        "acidity": RatingLevel.LOW,
        "body": RatingLevel.HIGH,
        "sweetness": RatingLevel.MEDIUM,
        "aroma": RatingLevel.MEDIUM,
        "bitterness": RatingLevel.MEDIUM,
    },
    {
        "name": "اتیوپی",
        "slug": "ethiopia",
        "image": "/media/origins/ethiopia.jpg",
        "flag": "/media/flags/ethiopia.png",
        "tasting": "گلی، مرکباتی\nو روشن",
        "order": 3,
        "acidity": RatingLevel.HIGH,
        "body": RatingLevel.LOW,
        "sweetness": RatingLevel.GOOD,
        "aroma": RatingLevel.HIGH,
        "bitterness": RatingLevel.LOW,
    },
]

TASTES = [
    ("میوه‌ای و شراب", "fruity", "fruity.webp", 2, 0),
    ("شکلاتی و کاراملی", "chocolate", "chocolate-caramel.webp", 3, 1),
    ("آجیلی و کاراملی", "nutty", "nutty-caramel.webp", 1, 2),
    ("گلی و شکوفه", "floral", "floral-blossom.webp", 3, 3),
    ("ملایم", "mild", "feather.webp", 3, 4),
    ("تلخ و قوی", "strong", "power.webp", 2, 5),
]

CONSUMPTION = [
    ("کم", "50 - 125 گرم", "کمتر از ۲ فنجان در روز", 1, 0),
    ("متوسط", "125 - 250 گرم", "۲ تا ۴ فنجان در روز", 2, 1),
    ("زیاد", "250 - 500 گرم", "۴ تا ۶ فنجان در روز", 3, 2),
    ("خیلی زیاد", "500 - 1000 گرم", "۶ تا ۱۰ فنجان در روز", 4, 3),
    ("حرفه ای", "بیشتر از 1000 گرم", "بیشتر از ۱۰ فنجان در روز", 5, 4),
]

PRODUCTS = [
    ("قهوه دانه دارکریست ستون", "darkroast-column-bean", "دانه", "۷۰۰ گرم", 1750000, "nik", True, 0),
    ("قهوه دانه دارکریست ستون", "darkroast-column-bean-2", "دانه", "۷۰۰ گرم", 1790000, "nik", True, 1),
    ("قهوه دانه دارکریست ستون", "darkroast-column-bean-3", "دانه", "۷۰۰ گرم", 1765000, "nik", True, 2),
    ("قهوه اسپرسو خانه ترکیبی", "home-espresso-blend", "اسپرسو", "۷۰ گرم", None, "motevaset", True, 3),
    ("قهوه اسپرسو خانه دارکریست ستون", "home-espresso-darkroast-1", "اسپرسو", "۱۰۰ گرم", None, "motevaset", True, 4),
    ("قهوه اسپرسوی خانه دارکریست ستون", "home-espresso-darkroast-2", "اسپرسو", "", 1390000, "motevaset", True, 5),
    ("قهوه اسپرسوی خانه دارکریست ستون", "home-espresso-darkroast-3", "اسپرسو", "", 1785000, "motevaset", True, 6),
    ("قهوه دانه دارکریست ویژه", "darkroast-special-bean", "دانه", "۱ کیلوگرم", 2450000, "nik", True, 7),
    ("قهوه اسپرسو کلاسیک", "espresso-classic", "اسپرسو", "۲۵۰ گرم", 980000, "motevaset", False, 8),
    ("قهوه دانه عربیکا", "arabica-bean", "دانه", "۵۰۰ گرم", 2100000, "nik", False, 9),
]


class Command(BaseCommand):
    help = "Seed brew methods, origins, tastes, consumption tiers and products."

    @transaction.atomic
    def handle(self, *args, **options):
        for name, slug, image, description, order in BREW_METHODS:
            BrewMethod.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "image": f"/media/brew_methods/{image}",
                    "description": description,
                    "order": order,
                },
            )

        for data in ORIGINS:
            Origin.objects.update_or_create(slug=data["slug"], defaults=data)

        for name, slug, image, rating, order in TASTES:
            TasteProfile.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "image": f"/images/tastes/{image}",
                    "rating": rating,
                    "order": order,
                },
            )

        for label, grams_range, hint, rating, order in CONSUMPTION:
            ConsumptionTier.objects.update_or_create(
                label=label,
                defaults={
                    "grams_range": grams_range,
                    "hint": hint,
                    "image": "/images/packet.webp",
                    "rating": rating,
                    "order": order,
                },
            )

        for (
            name,
            slug,
            type_label,
            weight,
            price,
            grade,
            is_bestseller,
            order,
        ) in PRODUCTS:
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "type_label": type_label,
                    "weight": weight,
                    "price": price,
                    "grade": grade,
                    "image": "☕",
                    "is_bestseller": is_bestseller,
                    "is_active": True,
                    "order": order,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded: %d brew methods, %d origins, %d tastes, %d tiers, %d products."
                % (
                    BrewMethod.objects.count(),
                    Origin.objects.count(),
                    TasteProfile.objects.count(),
                    ConsumptionTier.objects.count(),
                    Product.objects.count(),
                )
            )
        )
