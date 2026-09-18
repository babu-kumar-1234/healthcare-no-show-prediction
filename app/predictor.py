import json
import joblib
import pandas as pd


MODEL_PATH = "models/model.pkl"
THRESHOLD_PATH = "models/threshold.json"


# Load model
model = joblib.load(MODEL_PATH)


# Load threshold
with open(THRESHOLD_PATH, "r") as f:
    threshold_data = json.load(f)

THRESHOLD = float(threshold_data["threshold"])


def create_age_group(age):

    if pd.isna(age):
        return "Unknown"

    elif age <= 12:
        return "Child"

    elif age <= 19:
        return "Teen"

    elif age <= 39:
        return "Young Adult"

    elif age <= 59:
        return "Adult"

    elif age <= 74:
        return "Middle Age"

    else:
        return "75+"


def create_waiting_group(days):

    if pd.isna(days):
        return "Unknown"

    elif days == 0:
        return "Same Day"

    elif days <= 3:
        return "1-3 Days"

    elif days <= 7:
        return "4-7 Days"

    elif days <= 14:
        return "8-14 Days"

    elif days <= 30:
        return "15-30 Days"

    elif days <= 60:
        return "31-60 Days"

    else:
        return "61-180 Days"


def create_time_group(hour):

    if pd.isna(hour):
        return "Unknown"

    elif hour < 9:
        return "Morning"

    elif hour < 12:
        return "Late Morning"

    elif hour < 15:
        return "Afternoon"

    elif hour < 18:
        return "Evening"

    else:
        return "Late Evening"


def prepare_features(data):

    scheduled_day = pd.to_datetime(
        data["ScheduledDay"],
        utc=True
    )

    appointment_day = pd.to_datetime(
        data["AppointmentDay"],
        utc=True
    )

    waiting_days = (
        appointment_day.normalize()
        - scheduled_day.normalize()
    ).days

    if waiting_days < 0:
        waiting_days = None

    scheduled_hour = scheduled_day.hour

    scheduled_day_of_week = (
        scheduled_day.day_name()
    )

    appointment_day_of_week = (
        appointment_day.day_name()
    )

    appointment_month = appointment_day.month

    feature_data = {
        "Gender": data["Gender"],
        "Age": data["Age"],
        "Neighbourhood": data["Neighbourhood"],
        "Scholarship": data["Scholarship"],
        "Hipertension": data["Hipertension"],
        "Diabetes": data["Diabetes"],
        "Alcoholism": data["Alcoholism"],
        "Handcap": data["Handcap"],
        "SMS_received": data["SMS_received"],
        "WaitingDays": waiting_days,
        "ScheduledHour": scheduled_hour,
        "ScheduledDayOfWeek": scheduled_day_of_week,
        "AppointmentDayOfWeek": appointment_day_of_week,
        "AppointmentMonth": appointment_month,
        "AgeGroup": create_age_group(data["Age"]),
        "WaitingGroup": create_waiting_group(waiting_days),
        "ScheduledTimeGroup": create_time_group(
            scheduled_hour
        )
    }

    return pd.DataFrame([feature_data])


def predict_no_show(data):

    features = prepare_features(data)

    probability = model.predict_proba(
        features
    )[0][1]

    prediction = int(
        probability >= THRESHOLD
    )

    if prediction == 1:
        risk_level = "High Risk"
    else:
        risk_level = "Low Risk"

    return {
        "prediction": prediction,
        "probability": round(
            float(probability),
            4
        ),
        "risk_percentage": round(
            float(probability) * 100,
            2
        ),
        "risk_level": risk_level,
        "threshold": round(THRESHOLD, 2)
    }