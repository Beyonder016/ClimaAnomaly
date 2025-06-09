import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from app.data_collector import fetch_climate_data
from app.anomaly_detector import detect_anomalies
from app.forecast_model import forecast_climate_metric
from app.epic_fetcher import fetch_epic_thumbnails

# New imports for satellite map
import folium
from streamlit_folium import folium_static

# Page config
st.set_page_config(page_title='ClimaAnomaly', layout='wide')
st.title('🌍 ClimaAnomaly - Global Climate Monitoring & Forecasting')

# Sidebar Inputs
st.sidebar.header('🔧 Input Settings')

# Quick City Selector
cities = {
    'New York City': (40.7128, -74.0060),
    'London': (51.5074, -0.1278),
    'Tokyo': (35.6895, 139.6917),
    'San Francisco': (37.7749, -122.4194),
    'Paris': (48.8566, 2.3522),
    'Shanghai': (31.2304, 121.4737),
    'Dubai': (25.2048, 55.2708),
    'Singapore': (1.3521, 103.8198),
    'Hong Kong': (22.3193, 114.1694),
    'Beijing': (39.9042, 116.4074),
    'Mumbai': (19.0760, 72.8777),
    'Sydney': (-33.8688, 151.2093)
}
city_options = ['Custom'] + list(cities.keys())
selected_city = st.sidebar.selectbox('Quick Select City', city_options)
if selected_city != 'Custom':
    st.session_state['lat'], st.session_state['lon'] = cities[selected_city]

# Display current location name or coordinates
current_lat = st.session_state.get('lat', 18.5204)
current_lon = st.session_state.get('lon', 73.8567)
loc_label = selected_city if selected_city != 'Custom' else f"{current_lat:.6f}, {current_lon:.6f}"
st.sidebar.markdown(f"**Current Location:** {loc_label}")

# Coordinates Form: input both lat & lon and update on single submit
with st.sidebar.form('coord_form'):
    lat_input = st.number_input(
        'Latitude',
        value=current_lat,
        format='%.6f',
        help='Enter latitude in decimal degrees'
    )
    lon_input = st.number_input(
        'Longitude',
        value=current_lon,
        format='%.6f',
        help='Enter longitude in decimal degrees'
    )
    coord_submit = st.form_submit_button('Update Coordinates')

if coord_submit:
    st.session_state['lat'] = lat_input
    st.session_state['lon'] = lon_input
    st.sidebar.success('Coordinates updated!')

# Retrieve coords
lat = st.session_state.get('lat', 18.5204)
lon = st.session_state.get('lon', 73.8567)

# Other sidebar inputs
metric = st.sidebar.selectbox(
    'Metric to Analyze',
    ['T2M', 'RH2M', 'PRECTOTCORR', 'ALLSKY_SFC_SW_DWN']
)
years = st.sidebar.slider(
    'Years of History', min_value=1, max_value=5, value=2
)

# Compute date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * years)
start_str = start_date.strftime('%Y%m%d')
end_str = end_date.strftime('%Y%m%d')

# Main Dashboard
st.markdown('---')
st.subheader('📥 Fetching and Processing Climate Data')
load_state = st.text('Loading data...')

try:
    df = fetch_climate_data(lat, lon, start_str, end_str)
    if df is None or df.empty:
        raise ValueError('No data returned from API.')
    load_state.text('Data loaded successfully!')
except Exception as e:
    df = None
    load_state.text('Failed to load data.')
    st.error(f'❌ Failed to load climate data. Reason: {e}')

# Raw data toggle
if df is not None and st.checkbox('Show Raw Data'):
    st.write(df.tail())

if df is not None:
    # Date selector
    st.subheader('📅 Select Date to View (within loaded range)')
    valid_dates = df['DATE'].dt.date.drop_duplicates().tolist()
    selected_date = st.date_input(
        'Select a date',
        value=valid_dates[-1],
        min_value=valid_dates[0],
        max_value=valid_dates[-1]
    )

    # Anomaly Detection
    st.subheader('🚨 Anomaly Detection')
    anom_df = detect_anomalies(df, feature_cols=[metric])
    st.line_chart(anom_df.set_index('DATE')[[metric]])

    sel = anom_df[anom_df['DATE'].dt.date == selected_date]
    if not sel.empty:
        st.dataframe(sel[['DATE', metric, 'anomaly_flag']])
    else:
        st.warning('No data for selected date.')

    # Forecasting
    st.subheader('📈 Forecasting')
    forecast_df = forecast_climate_metric(df, metric=metric, forecast_days=30)
    st.line_chart(forecast_df.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']])

    # EPIC Imagery
    st.subheader('🛰️ EPIC Satellite Imagery')
    today = date.today()
    if selected_date >= today:
        st.warning('EPIC imagery not available for today/future dates.')
    else:
        try:
            images = fetch_epic_thumbnails(str(selected_date))
        except Exception as e:
            images = []
            st.error(f'Failed to fetch EPIC images: {e}')
        if images:
            cols = st.columns(min(3, len(images)))
            for idx, img in enumerate(images[:3]):
                with cols[idx]:
                    st.image(img['url'], caption=img['datetime'], use_container_width=True)
        else:
            st.warning('No EPIC images available for this date.')


# Footer
st.markdown('---')
st.caption('Built with ❤️ NASA POWER & EPIC APIs | Streamlit | Prophet | Sklearn | Folium')