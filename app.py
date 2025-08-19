from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from PIL import Image
import io
import numpy as np

from analysis import analyze_image
from style_rules import generate_style_recommendation

app = FastAPI(title="Style Sage API", version="0.1.0")

# CORS (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Survey(BaseModel):
    gender: Optional[str] = None
    ageRange: Optional[str] = None
    primaryOccasions: List[str] = []
    styleGoals: List[str] = []
    comfortVsAesthetic: Optional[str] = None
    colorPrefs: List[str] = []
    budget: Optional[str] = None

class AnalysisResponse(BaseModel):
    dominant_colors: List[Dict[str, Any]]
    brightness: float
    saturation: float
    palette_name: str
    style_profile: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    image: UploadFile = File(...),
    survey_json: str = Form(...),
):
    # Read and parse survey
    survey_dict = Survey.model_validate_json(survey_json)

    # Read image into PIL
    content = await image.read()
    pil_img = Image.open(io.BytesIO(content)).convert("RGB")

    # Analyze image (dominant colors, brightness, saturation, palette)
    img_stats = analyze_image(pil_img)

    # Combine with survey to make recommendations
    profile = generate_style_recommendation(img_stats, survey_dict.model_dump())

    return {
        **img_stats,
        "style_profile": profile,
    }
