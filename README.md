# 💰 Financial Analytics Dashboard

Interactive financial dashboard built with Python and Streamlit for visualizing transaction data and spending patterns.

## 🚀 Live Demo

- **Streamlit App**: [View Dashboard](https://financial-analytics-sarasaad.streamlit.app)

## ✨ Features

- 📊 Interactive visualizations (charts, maps, heatmaps)
- 🔍 Advanced filtering (year, product, transaction type)
- 💰 Real-time metrics and insights
- 🌍 Country comparison and geospatial analysis
- 📥 Data export capabilities

## 🛠️ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py
```

## 📋 Requirements

Python 3.8+, Streamlit, Pandas, Plotly, NumPy

## 📊 Data Format

CSV with columns: `Type`, `Product`, `Amount`, `Balance`, `Year`, `Month`, `Day`, `Weekday`, `Hour`, `Amount_Abs`, `Description_Anon`, `Merchant_Category`, `Country` (optional), `City` (optional)


## 🔒 Privacy

Public deployment uses dummy data. Real data is excluded via `.gitignore`.
