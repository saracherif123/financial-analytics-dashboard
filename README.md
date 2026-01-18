# Financial Dashboard - Interactive Analytics

A beautiful, interactive financial dashboard built with Python and Streamlit for visualizing transaction data.

## Features

- 📊 **Interactive Visualizations**: Multiple charts including balance over time, income vs expenses, category breakdowns, and more
- 🔍 **Advanced Filtering**: Filter by year, product type, and transaction type
- 💰 **Key Metrics**: Real-time calculation of balance, income, expenses, and net flow
- 📋 **Transaction Table**: View and explore recent transactions
- 📥 **Data Export**: Download filtered data as CSV

## Installation

1. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure the CSV file `Dataset - Sara Saad.csv` is in the same directory as `dashboard.py`

2. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. Run the Streamlit app:
```bash
streamlit run dashboard.py
```

3. The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Components

### Key Metrics
- Current Balance
- Total Income
- Total Expenses
- Net Flow

### Visualizations
1. **Balance Over Time**: Line chart showing account balance trends
2. **Monthly Income vs Expenses**: Bar chart comparing monthly income and expenses
3. **Expenses by Category**: Pie chart showing spending distribution
4. **Transaction Types Distribution**: Bar chart of transaction type frequencies
5. **Spending by Day of Week**: Bar chart showing spending patterns by weekday
6. **Spending by Hour of Day**: Line chart showing spending patterns throughout the day

### Filters
- Year selection
- Product type (Current, Savings, Deposit)
- Transaction type (Card Payment, Transfer, Topup, etc.)

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy

## Data Format

The dashboard expects a CSV file with the following columns:
- Type
- Product
- Amount
- Balance
- Year
- Month
- Day
- Weekday
- Hour
- Amount_Abs
- Description_Anon
- Merchant_Category

