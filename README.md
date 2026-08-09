# Spain Top 50 Music Intelligence Dashboard

Interactive Streamlit dashboard for analysing Spain Top 50 playlist lifecycle, content maturity, and churn.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The app expects these prepared files under `output/`:

- `clean_spain_top50.csv`
- `song_lifecycle.csv`
- `playlist_churn_analysis.csv`
- `research_summary.csv`

## Deploy to Streamlit Community Cloud

Push this project to GitHub, create a new app in Streamlit Community Cloud, and select `app.py` as the entry point. The included `requirements.txt` contains the required packages.
