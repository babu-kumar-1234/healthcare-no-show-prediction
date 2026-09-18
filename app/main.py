from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.prediction import router as prediction_router
from app.routes.health import router as health_router


app = FastAPI(
    title="Healthcare No-show Prediction API",
    description="Predicts appointment no-show risk using a Random Forest model.",
    version="1.0.0"
)


# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="app/templates"
)


# API routes
app.include_router(
    prediction_router
)

app.include_router(
    health_router
)


# Home page
@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )