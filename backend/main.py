from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import pickle
import os

app = FastAPI(title="Delhi Metro Crowd Predictor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/model.pkl")
with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)

model    = artifacts["model"]
le_stn   = artifacts["station_encoder"]
le_line  = artifacts["line_encoder"]
FEATURES = artifacts["features"]
CLASSES  = artifacts["classes"]
PEAK_HOURS = {8, 9, 10, 17, 18, 19}
INTERCHANGE = {"Rajiv Chowk", "Kashmere Gate", "Yamuna Bank", "INA"}

# ── Request / response models ────────────────────────────────
class PredictRequest(BaseModel):
    station:     str = Field(..., example="Rajiv Chowk")
    line:        str = Field(..., example="Yellow")
    hour:        int = Field(..., ge=5, le=23, example=9)
    day_of_week: int = Field(..., ge=0, le=6, example=0)

class PredictResponse(BaseModel):
    station:     str
    crowd_level: Literal["Low", "Medium", "High"]
    confidence:  float
    probabilities: dict

# ── Endpoints ────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "message": "Delhi Metro Crowd Predictor API"}

@app.get("/stations")
def get_stations():
    return {"stations": sorted(list(le_stn.classes_))}

@app.get("/lines")
def get_lines():
    return {"lines": sorted(list(le_line.classes_))}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if req.station not in le_stn.classes_:
        raise HTTPException(400, detail=f"Unknown station: {req.station}")
    if req.line not in le_line.classes_:
        raise HTTPException(400, detail=f"Unknown line: {req.line}")

    is_peak        = 1 if req.hour in PEAK_HOURS else 0
    is_weekend     = 1 if req.day_of_week in (5, 6) else 0
    is_interchange = 1 if req.station in INTERCHANGE else 0
    station_id     = le_stn.transform([req.station])[0]
    line_id        = le_line.transform([req.line])[0]

    X = [[req.hour, req.day_of_week, is_peak, is_weekend,
          is_interchange, station_id, line_id]]

    crowd_level    = model.predict(X)[0]
    proba          = model.predict_proba(X)[0]
    proba_dict     = {cls: round(float(p) * 100, 1) for cls, p in zip(CLASSES, proba)}

    return PredictResponse(
        station=req.station,
        crowd_level=crowd_level,
        confidence=round(max(proba) * 100, 1),
        probabilities=proba_dict
    )