# 🌍 ClimaAnomaly

[![Streamlit App](https://img.shields.io/badge/Demo-Link-blue?logo=streamlit)](https://climaanomaly.streamlit.app/)

ClimaAnomaly is a geospatial climate analytics dashboard that combines real-time weather data, anomaly detection, machine learning forecasting, and satellite imagery — all in one intuitive interface.

---

## ✨ Features

### 🔧 Smart Input Controls
- Select from major global cities or enter custom latitude and longitude
- Set the number of years of historical climate data to fetch
- Choose your climate metric: 
  - `T2M` (Air Temperature at 2m)
  - `RH2M` (Relative Humidity at 2m)
  - `PRECTOTCORR` (Precipitation)
  - `ALLSKY_SFC_SW_DWN` (Solar Radiation)

### 📊 Climate Insights
- **Anomaly Detection** using Z-score and Isolation Forest
- **30-day Forecasts** via Facebook Prophet with uncertainty intervals

### 🗺️ Interactive H3 Heatmap
- Uses [H3 Hexagonal Grid](https://h3geo.org/) for visualizing forecast data
- Customizable resolution and k-ring radius
- Colored hexes represent forecast value on chosen date
- Built with `folium`, `branca`, and `streamlit-folium`

### 🛰️ NASA EPIC Satellite Imagery
- Pulls near-Earth imagery for selected date from the DSCOVR-EPIC satellite
- Validates anomalies with visual evidence

---

## 📷 Demo Screens
| Forecast Heatmap | EPIC Satellite View |
|------------------|---------------------|
| ![](https://raw.githubusercontent.com/youruser/climaanomaly-assets/main/demo_map.png) | ![](https://raw.githubusercontent.com/youruser/climaanomaly-assets/main/demo_epic.png) |

---

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io)
- **Geospatial**: [H3-Py](https://github.com/uber/h3-py), [Folium](https://python-visualization.github.io/folium/), [Branca]
- **Backend**:
  - Data: [NASA POWER API](https://power.larc.nasa.gov/), [NASA EPIC API](https://epic.gsfc.nasa.gov/)
  - ML: [scikit-learn], [prophet]

---

## 🚀 Running Locally
```bash
# 1. Clone the repository
$ git clone https://github.com/youruser/climaanomaly.git
$ cd climaanomaly

# 2. (Optional) Create virtual environment
$ python -m venv venv
$ source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Launch app
$ streamlit run dashboard/dashboard_app.py
```

---

## 📌 Acknowledgements
- NASA POWER Data Services
- NASA EPIC Earth Imagery
- Uber H3 Library
- Streamlit and the open-source community

---

## 🌐 Live Now
📍 Visit the working app: [https://climaanomaly.streamlit.app](https://climaanomaly.streamlit.app)

---

## 📫 Feedback / Questions
Drop a message via Issues or reach out at [youremail@example.com]
