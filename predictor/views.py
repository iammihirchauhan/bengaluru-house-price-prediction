
from django.shortcuts import render
from django.db.models import Avg, Max

from .models import PredictionHistory
from ml.predict import predict_price, get_locations
from ml.model_metrics import model_metrics

def home(request):
    prediction = None
    error = None

    if request.method == "POST":
        try:
            area_type = request.POST.get("area_type")
            location = request.POST.get("location", "").strip()

            total_sqft = float(request.POST.get("total_sqft"))
            bath = int(request.POST.get("bath"))
            balcony = int(request.POST.get("balcony"))
            bhk = int(request.POST.get("bhk"))

            # Validate property details
            if not area_type or not location:
                raise ValueError("Please fill in all property details.")

            if total_sqft <= 0:
                raise ValueError("Area must be greater than zero.")

            if bath <= 0 or balcony < 0 or bhk <= 0:
                raise ValueError("Please enter valid BHK, bathroom and balcony values.")

            if total_sqft / bhk < 300:
                raise ValueError("Area per BHK is too small for a realistic prediction.")

            if bath > bhk + 2:
                raise ValueError("Please enter a realistic number of bathrooms.")

            # Predict house price
            prediction = predict_price(
                area_type,
                location,
                total_sqft,
                bath,
                balcony,
                bhk
            )

            # Save prediction history
            PredictionHistory.objects.create(
                area_type=area_type,
                location=location,
                total_sqft=total_sqft,
                bhk=bhk,
                bath=bath,
                balcony=balcony,
                predicted_price=prediction
            )

        except (ValueError, TypeError):
            error = "Please enter valid property details and try again."

    # Recent predictions
    history = list(
        PredictionHistory.objects.order_by("-created_at")[:10]
    )

    chart_labels = [item.location for item in reversed(history)]
    chart_prices = [item.predicted_price for item in reversed(history)]

    # Dashboard statistics
    total_predictions = PredictionHistory.objects.count()

    stats = PredictionHistory.objects.aggregate(
        average_price=Avg("predicted_price"),
        highest_price=Max("predicted_price")
    )

    latest_prediction = PredictionHistory.objects.order_by(
        "-created_at"
    ).first()

    return render(request, "predictor/home.html", {
        "prediction": prediction,
        "error": error,
        "history": history,
        "locations": get_locations(),
        "total_predictions": total_predictions,
        "average_price": stats["average_price"],
        "highest_price": stats["highest_price"],
        "latest_prediction": latest_prediction,
        "chart_labels": chart_labels,
        "chart_prices": chart_prices,
        "model_metrics": model_metrics,
    })
