from django.contrib import admin

from .models import (
    BrewMethod,
    ConsumptionTier,
    Origin,
    Product,
    TasteProfile,
    WizardSubmission,
)


@admin.register(WizardSubmission)
class WizardSubmissionAdmin(admin.ModelAdmin):
    list_display = ["id", "robusta", "method", "taste", "consumption", "recommended_origin", "created_at"]
    list_filter = ["method", "taste", "recommended_origin", "created_at"]
    date_hierarchy = "created_at"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "type_label", "weight", "price", "grade", "is_bestseller", "is_active"]
    list_filter = ["is_bestseller", "is_active", "grade", "type_label"]
    list_editable = ["is_bestseller", "is_active"]
    search_fields = ["name", "slug", "type_label"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(BrewMethod)
class BrewMethodAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    list_editable = ["order"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "acidity", "body", "sweetness", "aroma", "bitterness", "order"]
    list_editable = ["order"]
    list_filter = ["acidity", "body", "sweetness"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(TasteProfile)
class TasteProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "rating", "order"]
    list_editable = ["rating", "order"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(ConsumptionTier)
class ConsumptionTierAdmin(admin.ModelAdmin):
    list_display = ["label", "grams_range", "hint", "rating", "order"]
    list_editable = ["order"]
    search_fields = ["label"]
