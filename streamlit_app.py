import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',
)

REGIONS = {
    '전체': None,
    '아시아': ['CHN', 'JPN', 'KOR', 'IND', 'IDN', 'THA', 'VNM', 'MYS', 'SGP', 'PHL', 'BGD', 'PAK', 'MMR', 'LKA', 'KHM'],
    '유럽': ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD', 'POL', 'SWE', 'BEL', 'CHE', 'AUT', 'NOR', 'DNK', 'FIN', 'PRT', 'GRC', 'CZE', 'HUN', 'ROU', 'RUS'],
    '북아메리카': ['USA', 'CAN', 'MEX'],
    '남아메리카': ['BRA', 'ARG', 'COL', 'CHL', 'PER', 'VEN', 'ECU', 'BOL', 'URY', 'PRY'],
    '아프리카': ['ZAF', 'NGA', 'EGY', 'ETH', 'KEN', 'GHA', 'TZA', 'DZA', 'MAR', 'AGO', 'MOZ', 'CMR', 'CIV'],
    '중동': ['SAU', 'ARE', 'IRN', 'IRQ', 'TUR', 'ISR', 'QAT', 'KWT', 'OMN', 'JOR'],
    '오세아니아': ['AUS', 'NZL', 'PNG', 'FJI'],
}

UNIT_OPTIONS = {
    'Billion ($B)':  (1_000_000_000,   'B'),
    'Trillion ($T)': (1_000_000_000_000, 'T'),
    'Million ($M)':  (1_000_000,        'M'),
}


@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    code_to_name = dict(zip(raw_gdp_df['Country Code'], raw_gdp_df['Country Name']))

    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df['GDP'] = pd.to_numeric(gdp_df['GDP'], errors='coerce')

    return gdp_df, code_to_name


gdp_df, code_to_name = get_gdp_data()

'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

unit = st.radio('GDP 단위', list(UNIT_OPTIONS.keys()), horizontal=True)
divisor, unit_label = UNIT_OPTIONS[unit]

countries_in_data = set(gdp_df['Country Code'].unique())

region = st.selectbox('지역 필터', list(REGIONS.keys()))
if REGIONS[region] is not None:
    default_countries = [c for c in REGIONS[region] if c in countries_in_data][:6]
else:
    default_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']

all_countries = sorted(gdp_df['Country Code'].unique(), key=lambda c: code_to_name.get(c, c))

selected_codes = st.multiselect(
    'Which countries would you like to view?',
    options=all_countries,
    default=default_countries,
    format_func=lambda c: f'{code_to_name.get(c, c)} ({c})',
)

if not selected_codes:
    st.warning("Select at least one country")
    st.stop()

''
''
''

filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_codes))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
].copy()

filtered_gdp_df['GDP_display'] = filtered_gdp_df['GDP'] / divisor
filtered_gdp_df['Country'] = filtered_gdp_df['Country Code'].map(code_to_name)

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP_display',
    color='Country',
)

''
''

first_year_df = gdp_df[gdp_df['Year'] == from_year]
last_year_df = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_codes):
    col = cols[i % len(cols)]

    with col:
        first_rows = first_year_df[first_year_df['Country Code'] == country]['GDP']
        last_rows = last_year_df[last_year_df['Country Code'] == country]['GDP']

        first_gdp = first_rows.iloc[0] / divisor if len(first_rows) > 0 and not pd.isna(first_rows.iloc[0]) else float('nan')
        last_gdp = last_rows.iloc[0] / divisor if len(last_rows) > 0 and not pd.isna(last_rows.iloc[0]) else float('nan')

        country_name = code_to_name.get(country, country)

        if math.isnan(last_gdp):
            value_str = 'n/a'
            growth = 'n/a'
            delta_color = 'off'
        else:
            value_str = f'{last_gdp:,.2f}{unit_label}'
            if math.isnan(first_gdp) or first_gdp == 0:
                growth = 'n/a'
                delta_color = 'off'
            else:
                growth = f'{last_gdp / first_gdp:,.2f}x'
                delta_color = 'normal'

        st.metric(
            label=f'{country_name} ({country})',
            value=value_str,
            delta=growth,
            delta_color=delta_color,
        )
