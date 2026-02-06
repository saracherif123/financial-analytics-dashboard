# 💰 Financial Analytics Dashboard

An interactive personal finance dashboard built with **Streamlit** for visualizing spending patterns, analyzing financial health, and making data-driven financial decisions.

**Designed for**: Personal finance management, expense tracking, and geographic spending analysis across multiple locations and time periods.

---

## 📋 Table of Contents
1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Running the Dashboard](#running-the-dashboard)
5. [Project Structure](#project-structure)
6. [Data Format](#data-format)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 📊 Dashboard (Tab 1)
- **Key Metrics Cards**: Balance, Net Income, Savings Rate, Budget Status
- **Balance Trend**: Area chart showing balance evolution over time
- **Monthly Income vs Expenses**: Grouped bar chart with net flow line
- **Spending by Category**: Interactive bar chart with color intensity encoding

### 🔍 Spending Analysis (Tab 2)
- **Category Distribution**: Sunburst and treemap visualizations
- **Temporal Patterns**: Day-of-week and hourly spending heatmaps
- **Top Merchants**: Horizontal bar chart of top spending locations
- **Stacked Area Charts**: Category trends over time

### 🌍 Location Analysis (Tab 3)
- **Interactive World Map**: Country-level spending visualization
- **Country Comparison**: Bubble charts and trends by location
- **City-Level Breakdown**: Detailed city spending analysis

### 💳 Transaction Explorer (Tab 4)
- **Searchable Transaction Table**: Filter by merchant, category, or description
- **Data Export**: Download filtered transactions as CSV

### 🤖 AI Financial Advisor (Tab 5)
- **Natural Language Q&A**: Ask questions about spending patterns
- **Rule-based & AI-Powered**: Optional Google Gemini integration

### 📚 Methodology (Tab 6)
- **Complete Documentation**: Design choices and visual encodings
- **Data Structure**: Detailed explanation of all variables
- **Technology Stack**: Framework and library rationale

### 🎯 Filtering System
- **Date Range Picker**: Flexible time period selection
- **Year Selector**: Focus on specific years
- **Category Multi-Select**: Analyze specific expense categories
- **Type Filter**: Separate income vs expenses

---

## 🖥️ System Requirements

| Requirement | Minimum |
|---|---|
| **Python** | 3.8+ |
| **OS** | macOS, Linux, Windows |
| **RAM** | 2 GB |
| **Disk** | ~500 MB |

---

## 📦 Installation

### Step 1: Get the Code
```bash
cd financial-analytics-dashboard
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

### Start the App
```bash
streamlit run dashboard.py
```

The app opens automatically at `http://localhost:8501`

### Use Different Port
```bash
streamlit run dashboard.py --server.port 8502
```

---

## 📁 Project Structure

```
financial-analytics-dashboard/
├── dashboard.py                    # Main application
├── generate_dummy_data.py          # Generate sample data
├── Dataset - Dummy Data.csv        # Sample data (included)
├── .streamlit/
│   └── config.toml                 # Theme & settings
├── requirements.txt                # Dependencies
├── README.md                       # This file
└── venv/                           # Virtual environment
```

---

## 📊 Data Format

### Required CSV Columns
| Column | Type | Example |
|---|---|---|
| `Date` | datetime | 2023-01-15 |
| `Type` | string | Income / Expense |
| `Amount` | float | -50.00 |
| `Balance` | float | 1250.50 |
| `Product` | string | Card |
| `Description_Anon` | string | Merchant_X |
| `Merchant_Category` | string | Groceries |

### Auto-Generated Columns
- `Year`, `Month`, `Day`, `Weekday`, `Hour`, `Amount_Abs`

### Optional Columns
- `Country`, `City` (for geographic analysis)

### Use Your Own Data
1. Format CSV with required columns
2. Save as `Dataset - Dummy Data.csv` (same filename)
3. Run dashboard—data loads automatically

---

## ⚙️ Configuration

Edit `.streamlit/config.toml` to customize:
- **Colors**: Theme colors (Cyan, Magenta, Dark backgrounds)
- **Layout**: Wide mode for larger charts
- **Caching**: Auto-enabled for performance

### Enable AI (Optional)
```bash
export GEMINI_API_KEY="your_key"  # macOS/Linux
set GEMINI_API_KEY=your_key       # Windows
```



