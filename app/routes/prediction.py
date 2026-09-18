from fastapi import APIRouter
from app.schemas import AppointmentInput
from app.predictor import predict_no_show


router = APIRouter()


@router.post("/predict")
def predict(
    appointment: AppointmentInput
):

    result = predict_no_show(
        appointment.model_dump()
    )

    return result