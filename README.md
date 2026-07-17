# 🚔 Brooklyn 99 Analytics Dashboard

An interactive analytics dashboard exploring 8 seasons of *Brooklyn Nine-Nine* episode ratings, built with Python, SQL, and Streamlit.

**🔗 Live app:** [https://brooklyn99-sql-analytics-h6ht69gmohb4wop8mfwr4g.streamlit.app]



## About This Project

This dashboard analyzes every episode of Brooklyn Nine-Nine across 8 seasons, surfacing patterns in critical reception, season-over-season quality, and the gap between popularity and appreciation. It started as a Tableau project, but after persistent friction with dual-axis charts, filter behavior, and a data source connection that eventually corrupted unsaved work, I rebuilt it as a Python/Streamlit app — a decision that ended up teaching me a lot more about the underlying mechanics of interactive dashboards than a drag-and-drop tool would have.

## What It Shows

- **Rating Trend** — every episode's rating over the course of the series, color-coded by category (Masterpiece / Great / Average / Weak), with a dynamic average reference line
- **Season Comparison** — which seasons improved from first episode to last
- **Rating Distribution** running average rating within each season
- **Cult Favorites** — episodes that were critically loved but under-watched, versus episodes that were popular but less acclaimed, based on comparing rating rank against vote-count rank
- **Holiday Episode Analysis** — whether Brooklyn 99's holiday episodes actually outperform regular episodes

All charts respond to a season filter in the sidebar, so you can isolate and compare specific seasons across every view.

## Tech Stack

- **Python** — pandas for data wrangling
- **SQLite** — used via `sqlite3` for window functions (running averages, rankings) during data prep
- **Streamlit** — app framework and interactivity
- **Plotly** — interactive charting
- **Streamlit Community Cloud** — deployment

## Data Pipeline

Raw episode data was cleaned and enriched using SQL queries (running averages, popularity/appreciation rankings, episode categorization) executed against an in-memory SQLite database, then exported to flat CSVs that power this app.



## Project Structure

```
brooklyn99-sql-analytics/
├── data/                  # source data
├── exports/               # cleaned CSVs used by the dashboard
├── notebooks/             # SQL data prep and export notebook
└── dashboard/
    └── app.py             # Streamlit dashboard
    └── .streamlit/
        └── config.toml     # custom theme
├── requirements.txt      
```

## What I Learned

This project doubled as a hands-on introduction to Python-based dashboarding after several years working primarily in Tableau, Power BI, and Qlik Sense. Highlights included:

- Recreating dual-axis and diverging-color chart logic that required significant manual configuration in Tableau using a few lines of Plotly (`color_continuous_midpoint`, `add_hline`)
- Understanding Streamlit's rerun-based execution model and where caching (`@st.cache_data`) matters
- Deploying to the cloud and debugging the gap between "works locally" and "works in a fresh environment" (path case-sensitivity, missing dependencies)

