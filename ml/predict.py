import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

model = joblib.load(ARTIFACTS_DIR / "house_price_model.pkl")
preprocessor = joblib.load(ARTIFACTS_DIR / "preprocessor.pkl")
common_locations = joblib.load(ARTIFACTS_DIR / "common_locations.pkl")


def predict_price(area_type, location, total_sqft, bath, balcony, bhk):

    if location not in common_locations:
        location = "Other"

    input_data = pd.DataFrame(
        [
            {
                "area_type": area_type,
                "location": location,
                "total_sqft": total_sqft,
                "bath": bath,
                "balcony": balcony,
                "bhk": bhk,
            }
        ]
    )

    processed_data = preprocessor.transform(input_data)
    prediction = model.predict(processed_data)

    return round(prediction[0], 2)


def get_locations():
    return sorted(common_locations)
