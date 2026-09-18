from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date


class AppointmentInput(BaseModel):

    Gender: str

    Age: float = Field(
        ...,
        ge=0,
        le=100
    )

    Neighbourhood: str

    Scholarship: int = Field(
        ...,
        ge=0,
        le=1
    )

    Hipertension: int = Field(
        ...,
        ge=0,
        le=1
    )

    Diabetes: int = Field(
        ...,
        ge=0,
        le=1
    )

    Alcoholism: int = Field(
        ...,
        ge=0,
        le=1
    )

    Handcap: int = Field(
        ...,
        ge=0,
        le=4
    )

    SMS_received: int = Field(
        ...,
        ge=0,
        le=1
    )

    ScheduledDay: datetime

    AppointmentDay: date

    @field_validator("AppointmentDay")
    @classmethod
    def validate_appointment_date(
        cls,
        appointment_day,
        info
    ):

        scheduled_day = info.data.get(
            "ScheduledDay"
        )

        if scheduled_day is not None:

            if appointment_day < scheduled_day.date():

                raise ValueError(
                    "Appointment date cannot be before scheduled date."
                )

        return appointment_day