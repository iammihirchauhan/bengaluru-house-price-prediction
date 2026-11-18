from django.db import models


class PredictionHistory(models.Model):
    area_type = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    total_sqft = models.FloatField()
    bhk = models.IntegerField()
    bath = models.IntegerField()
    balcony = models.IntegerField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - ₹{self.predicted_price} Lakhs"