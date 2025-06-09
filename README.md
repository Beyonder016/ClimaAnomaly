# 🌍 ClimaAnomaly

**Real-Time Global Climate Monitoring & Forecasting Tool**

---

## 📢 Overview

ClimaAnomaly is a fully open-source and free-to-deploy system that fetches **real-time global climate data** from NASA POWER APIs, detects **climate anomalies**, and forecasts **future trends**. It integrates satellite imagery from NASA EPIC to visually support anomaly dates, and displays everything in a sleek **Streamlit dashboard**.

---

## 🚀 Features

- 📡 Real-time NASA POWER API integration for daily climate variables
- ⚠️ Anomaly detection using Z-score and Isolation Forest
- 📈 30-day forecasting using Facebook Prophet
- 🛰️ Satellite image thumbnails from NASA EPIC
- 📊 Interactive Streamlit dashboard with time-series plots, maps, and more
- 💾 Local data caching for speed and API efficiency

---

## 📦 Project Structure

```
ClimaAnomaly/
├── app/
│   ├── data_collector.py         # NASA POWER data fetcher
│   ├── anomaly_detector.py       # Anomaly detection module
│   ├── forecast_model.py         # Prophet-based forecasting
│   ├── epic_fetcher.py           # NASA EPIC imagery fetcher
│   └── __init__.py
│
├── dashboard/
│   └── dashboard_app.py          # Main Streamlit UI
│
├── data_cache/                  # Cached data (auto-created)
├── models/                      # Saved Prophet models
├── docs/                        # Diagrams and documentation (optional)
├── requirements.txt             # Python dependencies
└── README.md                    # You are here
```

---

## 📥 Installation & Local Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ClimaAnomaly.git
cd ClimaAnomaly
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard

```bash
streamlit run dashboard/dashboard_app.py
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push this project to a **public GitHub repo**
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and log in
3. Deploy your app:

   - **Repository:** `yourusername/ClimaAnomaly`
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard_app.py`

You're live 🎉

---

## 🔧 Technologies Used

| Area              | Tech/Library                             |
| ----------------- | ---------------------------------------- |
| Climate API       | NASA POWER                               |
| Satellite Imagery | NASA EPIC                                |
| Anomaly Detection | scikit-learn (Isolation Forest), Z-score |
| Forecasting       | Prophet (Facebook)                       |
| Web App           | Streamlit                                |
| Data Handling     | Pandas, NumPy                            |

---

## 📍 Sample Use Case

> A researcher in India wants to know whether recent rainfall was unusual. ClimaAnomaly fetches past 2 years of rainfall data, detects an anomaly spike last week, forecasts the next 30 days, and provides satellite imagery for that date.

---

## 🙋‍♂️ Maintainers

- [Your Name](https://github.com/yourusername)

PRs and feedback welcome!

---

## 📄 License

MIT License
