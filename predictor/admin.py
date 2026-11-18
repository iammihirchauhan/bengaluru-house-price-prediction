from django.contrib import admin
from .models import PredictionHistory


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "location",
        "area_type",
        "total_sqft",
        "bhk",
        "predicted_price",
        "created_at",
    )
    list_filter = ("area_type", "created_at")
    search_fields = ("location",)
