# :earth_americas: GDP dashboard

A Streamlit app for exploring GDP data of countries around the world, sourced from the [World Bank Open Data](https://data.worldbank.org/).

## Features

- **Country name display** — shows full country names (e.g. Germany (DEU)) in selectors, chart legend, and metric cards
- **Year range slider** — filter data by start and end year (1960–2022)
- **GDP unit selector** — switch between Billion ($B), Trillion ($T), and Million ($M)
- **Regional filter** — quickly select countries by region (아시아, 유럽, 북아메리카, 남아메리카, 아프리카, 중동, 오세아니아)
- **GDP trend chart** — line chart showing GDP over time per country
- **GDP metric cards** — shows latest GDP value and growth multiple vs. the start year
- **Safe missing data handling** — gracefully handles years/countries with no GDP data

## How to run

### Option 1 — uv (recommended)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a Python 3.12 virtual environment and install dependencies
uv venv --python 3.12 .venv
uv pip install -r requirements.txt --python .venv/bin/python

# Run the app
.venv/bin/streamlit run streamlit_app.py
```

### Option 2 — standard venv

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run streamlit_app.py
```

Open **http://localhost:8501** in your browser.
