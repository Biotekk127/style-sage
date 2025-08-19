# Style Sage – AI Style Recommender (MVP)

This is a complete, runnable MVP for your AI style website:
- **Frontend**: Next.js (React) single-page app for upload + quick survey.
- **Backend**: FastAPI service that analyzes the uploaded outfit photo and merges it with survey answers to produce a style profile.

> NOTE: This MVP uses a **lightweight rule-based engine** + dominant color analysis from the image. You can later swap in ML models for clothing detection, body segmentation, etc.

## Quick Start (Docker)

1) Create an `.env` file in `frontend/` (optional) with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

2) Build and run both services:
```
docker compose up --build
```

3) Open the app:
- Frontend: http://localhost:3000
- Backend:  http://localhost:8000/docs

## Manual Start (without Docker)

### Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend
```
cd frontend
npm install
# Create .env.local for the frontend API URL:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## How it Works

- The backend accepts a multipart POST to `/analyze` with `image` (file) and `survey_json` (stringified JSON).
- `analysis.py` extracts dominant colors, brightness, and saturation via fast image quantization and HSV math.
- `style_rules.py` maps the image palette + survey (occasions, goals, colors) into a ranked list of styles, fit tips, and a beginner capsule.

## Evolving this MVP

- Add real **clothing detection** (top/bottom/shoes) via a vision model (e.g., YOLOv8 trained on DeepFashion2).
- Add **body landmarks** and **silhouette analysis** (e.g., MediaPipe) to tailor fit recommendations.
- Replace `style_rules.py` with a trainable **recommender** that learns from user ratings.
- Implement **accounts** and save profiles.
- Monetize with **affiliate links** and a **premium Pro tier** for advanced looks/virtual try-on.

## Security & Privacy Notes

- Never store user images unencrypted in production.
- Add max file size limits, virus scanning, signed URLs, and auth.
- Update CORS to specific origins in `app.py`.

---

Made with ❤️ as a starting point for your startup.
