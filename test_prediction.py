from ml.predict import predict_price

price = predict_price(
    area_type="Super built-up  Area",
    location="Unknown Location",
    total_sqft=1200,
    bath=2,
    balcony=1,
    bhk=2
)

print("Predicted House Price:", price, "Lakhs")