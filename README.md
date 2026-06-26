# 🚇 Delhi Metro Crowd Predictor

> Predicts crowd levels at Delhi Metro stations using time-of-day and
> station patterns. Built with FastAPI + React + scikit-learn.

**[Live Demo](https://your-app.vercel.app)** | [API Docs](https://your-api.railway.app/docs)

## What it does
- Predicts Low / Medium / High crowd at any station + time combination
- 87% test accuracy (Random Forest, 7 features, 1.3M training rows)
- Real-time predictions via FastAPI REST API

## Tech stack
| Layer      | Technology              |
|------------|-------------------------|
| ML Model   | scikit-learn RandomForest|
| Backend    | FastAPI + Python 3.11   |
| Frontend   | React 18 + Vite         |
| Deployment | Railway + Vercel        |

## Architecture
[simple ASCII or image diagram]

## How crowd levels are defined
| Level  | Passengers/hr | Condition         |
|--------|---------------|-------------------|
| Low    | < 260         | Comfortable ride  |
| Medium | 260–480       | Moderately full   |
| High   | > 480         | Very crowded      |

## Feature importance
| Feature        | Importance |
|----------------|------------|
| hour           | 0.34       |
| is_peak        | 0.28       |
| station_id     | 0.19       |
| day_of_week    | 0.09       |
| is_interchange | 0.05       |
| is_weekend     | 0.03       |
| line_id        | 0.02       |

## Run locally
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Data note
DMRC does not publish ridership data publicly.
This project uses synthetic data generated from known peak-hour
patterns (morning rush 8–10am, evening rush 5–7pm) and DMRC
timetable information.

## Author
Om Kartike —