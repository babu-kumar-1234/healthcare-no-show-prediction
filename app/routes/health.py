from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Healthcare No-show Prediction API"
    }