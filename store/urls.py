from django.urls import path

from . import views

urlpatterns = [
    # Storefront
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("bestsellers/", views.bestsellers, name="bestsellers"),
    # Wizard options
    path("wizard/options/", views.wizard_options, name="wizard_options"),
    path("methods/", views.brew_method_list, name="brew_method_list"),
    path("origins/", views.origin_list, name="origin_list"),
    path("tastes/", views.taste_list, name="taste_list"),
    path("consumption/", views.consumption_list, name="consumption_list"),
    # Wizard outcome
    path("recommend/", views.recommend, name="recommend"),
    path("csrf/", views.csrf_token, name="csrf_token"),
]
