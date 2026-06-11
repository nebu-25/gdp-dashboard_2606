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

---

## 이슈 관리

### ✅ 해결된 이슈

| 날짜 | 이슈 | 해결 방법 |
|---|---|---|
| 2026-06-11 | `.gitattributes` 파일이 미추적 상태로 방치됨 | 커밋 후 푸시 완료 |
| 2026-06-11 | `.gitignore` 미설정으로 내부 도구 파일 노출 위험 | `.gitignore` 업데이트 완료 (`.claude/` 추가) |

### 🔶 알려진 이슈 (미해결)

| 우선순위 | 이슈 | 설명 |
|---|---|---|
| 중간 | **데이터 최신화 불가** | World Bank 데이터셋이 1960–2022년으로 고정되어 있어 실시간 갱신 불가 |
| 낮음 | **Streamlit Cloud 미배포** | 현재 로컬 실행만 가능, 공개 URL 없음 |
