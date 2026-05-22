# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-based web application for AI/ML expert models. Currently implements a Titanic survival prediction system using a TensorFlow neural network. The project is structured to support multiple AI models (medical, accounts, core apps are scaffolded but not yet implemented).

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Run tests for a specific app
python manage.py test accidents_ai

# Retrain the ML model (from project root)
cd accidents_ai/ml && python train_model.py
```

## Architecture

### Django Apps

- **accidents_ai** — The only functional app. Predicts Titanic passenger survival via a web form. Has no database models; all state is in the ML model files.
- **medical_ai**, **accounts**, **core** — Scaffolded but empty; not yet implemented.

### ML Pipeline (`accidents_ai/`)

```
accidents_ai/
├── ml/
│   ├── train_model.py   # Training script: reads titanic.csv, outputs model.keras + encoder.pkl
│   ├── model.keras      # Trained sequential network: 32 → 16 → 1 neurons (sigmoid output)
│   └── encoder.pkl      # Fitted ColumnTransformer (StandardScaler + OneHotEncoder)
├── services/
│   └── predictor.py     # Loads model/encoder at import time, exposes predict()
├── forms.py             # Django form matching the 9 prediction input fields
└── views.py             # Calls predictor.predict() and renders result in form.html
```

The predictor service loads `model.keras` and `encoder.pkl` once at module import. When retraining, restart the dev server so the new artifacts are reloaded.

### URL Routing

- `/` — redirects or home (see `modelos_expertos/urls.py`)
- `/accidentes/` — Titanic prediction form (`accidents_ai/urls.py`)
- `/admin/` — Django admin

### Input Features for Prediction

`sex`, `age`, `n_siblings_spouses`, `parch`, `fare`, `passenger_class`, `deck`, `embark_town`, `alone`

## Key Configuration

- **Database**: SQLite (`db.sqlite3`) — already migrated, no setup needed for local dev.
- **Python version**: 3.12 (specified in `mise.toml`).
- **ML artifacts** are git-ignored (`*.keras`, `*.pkl`) — run `train_model.py` to regenerate them if missing.
- `SECRET_KEY` and `DEBUG=True` are hardcoded in `settings.py`; move to environment variables before any deployment.
