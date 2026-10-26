# SmartJohad AI

**AI-assisted preliminary design and risk screening for traditional johads.**

This educational Streamlit prototype modernizes traditional Indian rainwater-harvesting ideas with transparent preliminary engineering calculations and screening prompts.

## Features

- Estimate rainfall-event runoff using catchment area, rainfall depth, and a selected runoff coefficient.
- Calculate simplified trapezoidal embankment geometry and approximate fill volume.
- Visualize a conceptual cross-section.
- Flag items needing review, including spillway, freeboard, soil properties, seepage, and stability.
- Export screening results to CSV.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
2. Create an app from this repository's `main` branch.
3. Set the main file path to `app.py` and deploy.

## Safety and limitations

This is not a construction-ready design, structural safety certification, or validated AI model. Screening flags are prompts, not calculated factors of safety. Real structures require surveyed topography and storage, design-storm analysis and flow routing, geotechnical investigation, applicable standards, and qualified professional review. Do not construct or modify a real structure based on this prototype.
