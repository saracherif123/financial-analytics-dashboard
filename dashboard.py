import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Financial Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS with Vibrant Accents
st.markdown("""
    <style>
    /* Ensure sidebar is always accessible */
    [data-testid="stSidebar"] {
        position: fixed !important;
    }
    
    /* Sidebar toggle button always visible */
    [data-testid="stSidebar"] [data-testid="collapsedControl"] {
        display: block !important;
    }
    
    /* Reset button styling - smaller and black text - more specific */
    [data-testid="stSidebar"] button {
        font-size: 0.65rem !important;
    }
    
    [data-testid="stSidebar"] button > div,
    [data-testid="stSidebar"] button > div > p,
    [data-testid="stSidebar"] button > div > span {
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 0.65rem !important;
    }
    
    [data-testid="stSidebar"] button:hover > div,
    [data-testid="stSidebar"] button:hover > div > p,
    [data-testid="stSidebar"] button:hover > div > span {
        color: #000000 !important;
    }
    
    /* Force black text on all button content */
    [data-testid="stSidebar"] button * {
        color: #000000 !important;
    }
    
    /* Reset button styling - smaller text and black */
    [data-testid="stSidebar"] button {
        font-size: 0.65rem !important;
    }
    
    /* Force black text on button - override white text rule */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button > div,
    [data-testid="stSidebar"] button > div > p,
    [data-testid="stSidebar"] button > div > span,
    [data-testid="stSidebar"] button > div > div {
        color: #000000 !important;
        font-size: 0.65rem !important;
    }
    
    [data-testid="stSidebar"] button:hover,
    [data-testid="stSidebar"] button:hover > div,
    [data-testid="stSidebar"] button:hover > div > p,
    [data-testid="stSidebar"] button:hover > div > span {
        color: #000000 !important;
    }
    
    /* Override any white text rules for buttons */
    [data-testid="stSidebar"] button * {
        color: #000000 !important;
    }
    
    /* Improve sidebar styling */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Better filter spacing */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stNumberInput {
        margin-bottom: 1rem;
    }
    
    /* Original styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Section Headers */
    h2 {
        color: #00f5ff;
        font-weight: 700;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }
    
    h3 {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Sidebar - Ensure it's visible and scrollable */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Make sidebar scrollable - target the content area */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: calc(100vh - 3rem) !important;
        padding-bottom: 2rem !important;
    }
    
    /* Ensure sidebar content can scroll */
    section[data-testid="stSidebar"] {
        overflow: visible !important;
    }
    
    section[data-testid="stSidebar"] > div {
        overflow-y: auto !important;
        max-height: 100vh !important;
    }
    
    /* Sidebar toggle button - make it more visible */
    [data-testid="collapsedControl"] {
        background: rgba(0, 245, 255, 0.2) !important;
        border: 1px solid rgba(0, 245, 255, 0.5) !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(0, 245, 255, 0.3) !important;
    }
    
    /* Sidebar toggle button icon/arrow - white - use filter */
    [data-testid="collapsedControl"] svg {
        filter: brightness(0) invert(1) !important;
        color: #ffffff !important;
    }
    
    /* Also target all SVG elements */
    [data-testid="collapsedControl"] svg *,
    [data-testid="collapsedControl"] svg path,
    [data-testid="collapsedControl"] svg circle,
    [data-testid="collapsedControl"] svg line,
    [data-testid="collapsedControl"] svg polyline,
    [data-testid="collapsedControl"] svg g {
        fill: #ffffff !important;
        stroke: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Force white on all child elements */
    [data-testid="collapsedControl"] * {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #a0a0a0;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        color: #000000;
        font-weight: 700;
    }
    
    /* Sidebar - Reduce spacing between elements - more aggressive */
    [data-testid="stSidebar"] h3 {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    [data-testid="stSidebar"] h2 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.25rem !important;
        display: block !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] hr {
        margin: 0.25rem 0 !important;
    }
    
    [data-testid="stSidebar"] p {
        margin: 0.1rem 0 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stButton {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stNumberInput > div,
    [data-testid="stSidebar"] .stDateInput > div,
    [data-testid="stSidebar"] .stButton > div {
        margin-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Reduce spacing for markdown elements in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        margin: 0.05rem 0 !important;
    }
    
    /* Reduce spacing in vertical blocks */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="element-container"] {
        margin-bottom: 0.1rem !important;
        padding-bottom: 0 !important;
    }
    
    /* Reduce spacing between columns */
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0.1rem !important;
    }
    
    /* Sidebar - Labels and text white, but input values black */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] p:not(button p),
    [data-testid="stSidebar"] strong,
    [data-testid="stSidebar"] label:not(button label),
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2 {
        color: #ffffff !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Buttons in sidebar should have black text - override white text */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button * {
        color: #000000 !important;
    }
    
    /* Date input field values - black for readability */
    [data-testid="stSidebar"] .stDateInput input,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="input"],
    [data-testid="stSidebar"] .stDateInput [data-baseweb="input"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Number input field values - black for readability */
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stNumberInput [data-baseweb="input"],
    [data-testid="stSidebar"] .stNumberInput [data-baseweb="input"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Selectbox selected value - black for readability */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Sidebar selectbox dropdown text */
    [data-baseweb="popover"] [data-baseweb="select"] {
        color: #000000 !important;
    }
    
    /* Dataframes */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle visible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Keep header visible but minimal - needed for sidebar toggle */
    header {
        visibility: visible !important;
        height: 3rem !important;
    }
    
    /* Make sidebar toggle button very visible */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
        background: rgba(0, 245, 255, 0.2) !important;
        border: 2px solid rgba(0, 245, 255, 0.6) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 8px !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(0, 245, 255, 0.4) !important;
        border-color: rgba(0, 245, 255, 1) !important;
    }
    
    /* Sidebar toggle button icon/arrow - white - use filter */
    [data-testid="collapsedControl"] svg {
        filter: brightness(0) invert(1) !important;
        color: #ffffff !important;
    }
    
    /* Also target all SVG elements */
    [data-testid="collapsedControl"] svg *,
    [data-testid="collapsedControl"] svg path,
    [data-testid="collapsedControl"] svg circle,
    [data-testid="collapsedControl"] svg line,
    [data-testid="collapsedControl"] svg polyline,
    [data-testid="collapsedControl"] svg g {
        fill: #ffffff !important;
        stroke: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Force white on all child elements */
    [data-testid="collapsedControl"] * {
        color: #ffffff !important;
    }
    
    /* Sidebar visibility */
    [data-testid="stSidebar"] {
        visibility: visible !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        border-radius: 5px;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(0, 245, 255, 0.1);
        border-left: 4px solid #00f5ff;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Configuration
DATA_SOURCE = 'dummy'

# Load data - cache includes file modification time to auto-refresh
@st.cache_data(ttl=60, show_spinner=False)
def load_data(file_mtime=0):
    import os
    if DATA_SOURCE == 'dummy':
        data_file = 'Dataset - Dummy Data.csv'
    else:
        data_file = 'Dataset - Sara Saad.csv'
    
    try:
        df = pd.read_csv(data_file)
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
        df['Amount_Abs'] = pd.to_numeric(df['Amount_Abs'], errors='coerce')
        
        # Ensure Weekday and Hour columns exist (create from Date if missing)
        if 'Weekday' not in df.columns:
            df['Weekday'] = df['Date'].dt.day_name()
        if 'Hour' not in df.columns:
            df['Hour'] = df['Date'].dt.hour
        
        if 'Country' not in df.columns:
            df['Country'] = 'Unknown'
        if 'City' not in df.columns:
            df['City'] = 'Unknown'
        return df
    except FileNotFoundError:
        try:
            fallback_file = 'Dataset - Dummy Data.csv' if DATA_SOURCE == 'real' else 'Dataset - Sara Saad.csv'
            df = pd.read_csv(fallback_file)
            df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
            df['Amount_Abs'] = pd.to_numeric(df['Amount_Abs'], errors='coerce')
            
            # Ensure Weekday and Hour columns exist (create from Date if missing)
            if 'Weekday' not in df.columns:
                df['Weekday'] = df['Date'].dt.day_name()
            if 'Hour' not in df.columns:
                df['Hour'] = df['Date'].dt.hour
            
            if 'Country' not in df.columns:
                df['Country'] = 'Unknown'
            if 'City' not in df.columns:
                df['City'] = 'Unknown'
            st.info("Using fallback data file")
            return df
        except Exception as e2:
            st.error("Error: Could not find data file.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data - include file modification time to auto-refresh cache when file changes
import os
data_file = 'Dataset - Dummy Data.csv' if DATA_SOURCE == 'dummy' else 'Dataset - Sara Saad.csv'
file_mtime = int(os.path.getmtime(data_file)) if os.path.exists(data_file) else 0
df = load_data(file_mtime=file_mtime)

if df is not None:
    # Header
    st.markdown('<h1 class="main-header">Financial Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Interactive Transaction Analytics & Insights</p>', unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown("### 📊 FILTERS")
    
    # Reset filters button at the top of filters
    col_reset1, col_reset2 = st.sidebar.columns(2)
    with col_reset1:
        if st.sidebar.button("🔄 Reset", key="reset_filters", use_container_width=True):
            # Clear all filter keys from session state to reset to defaults
            for key in ['start_date', 'end_date', 'year_filter', 'product_filter', 'type_filter', 'category_filter']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col_reset2:
        if st.sidebar.button("🗑️ Clear Cache", key="clear_cache", use_container_width=True):
            # Clear the data cache
            load_data.clear()
            st.rerun()
    
    # Sidebar Filters
    st.sidebar.markdown("### 📊 FILTERS")
    
    # Date Range - Improved handling
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    st.sidebar.markdown("**Date Range**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="start_date",
            label_visibility="collapsed"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="end_date",
            label_visibility="collapsed"
        )
    
    # Ensure start_date <= end_date
    if start_date > end_date:
        st.sidebar.warning("Start date must be before end date. Adjusting...")
        start_date, end_date = min_date, max_date
    
    # Apply date range filter first to get available options for other filters
    date_filtered_df = df[
        (df['Date'].dt.date >= start_date) & 
        (df['Date'].dt.date <= end_date)
    ].copy()
    
    # Year filter - populate from date-filtered data
    st.sidebar.markdown("**Year**")
    if len(date_filtered_df) > 0:
        years = ['All'] + sorted(date_filtered_df['Year'].unique().tolist())
    else:
        years = ['All'] + sorted(df['Year'].unique().tolist())
    
    # Get current selection or default to 'All'
    current_year = st.session_state.get('year_filter', 'All')
    if current_year not in years:
        current_year = 'All'
    
    selected_year = st.sidebar.selectbox(
        "Select Year",
        years,
        index=years.index(current_year),
        key="year_filter",
        label_visibility="collapsed"
    )
    
    # Account Type filter - populate from date-filtered data
    st.sidebar.markdown("**Account Type**")
    if len(date_filtered_df) > 0:
        products = ['All'] + sorted(date_filtered_df['Product'].unique().tolist())
    else:
        products = ['All'] + sorted(df['Product'].unique().tolist())
    
    # Get current selection or default to 'All'
    current_product = st.session_state.get('product_filter', 'All')
    if current_product not in products:
        current_product = 'All'
    
    selected_product = st.sidebar.selectbox(
        "Select Account Type",
        products,
        index=products.index(current_product),
        key="product_filter",
        label_visibility="collapsed",
        help="Current, Savings, or Deposit account"
    )
    
    # Transaction Type filter - populate from date-filtered data
    st.sidebar.markdown("**Transaction Type**")
    if len(date_filtered_df) > 0:
        types = ['All'] + sorted(date_filtered_df['Type'].unique().tolist())
    else:
        types = ['All'] + sorted(df['Type'].unique().tolist())
    
    # Get current selection or default to 'All'
    current_type = st.session_state.get('type_filter', 'All')
    if current_type not in types:
        current_type = 'All'
    
    selected_type = st.sidebar.selectbox(
        "Select Transaction Type",
        types,
        index=types.index(current_type),
        key="type_filter",
        label_visibility="collapsed"
    )
    
    # Category filter - populate from date-filtered data
    st.sidebar.markdown("**Category**")
    if len(date_filtered_df) > 0:
        categories = ['All'] + sorted(date_filtered_df['Merchant_Category'].unique().tolist())
    else:
        categories = ['All'] + sorted(df['Merchant_Category'].unique().tolist())
    
    # Get current selection or default to 'All'
    current_category = st.session_state.get('category_filter', 'All')
    if current_category not in categories:
        current_category = 'All'
    
    selected_category = st.sidebar.selectbox(
        "Select Category",
        categories,
        index=categories.index(current_category),
        key="category_filter",
        label_visibility="collapsed"
    )
    
    # Budget variable (for use in dashboard, but not shown in sidebar)
    monthly_budget = 1000
    
    # Apply all filters sequentially
    filtered_df = df.copy()
    
    if len(filtered_df) > 0:
        # Date range filter
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
        
        # Year filter
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
        
        # Account Type filter
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
        
        # Transaction Type filter
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Type'] == selected_type]
    
        # Category filter
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Merchant_Category'] == selected_category]
    
    # Calculate metrics with error handling
    if len(filtered_df) > 0:
        # Sort by date to ensure last balance is correct
        filtered_df = filtered_df.sort_values('Date').reset_index(drop=True)
        # Get the most recent balance (last row after sorting by date)
        current_balance = float(filtered_df['Balance'].iloc[-1]) if len(filtered_df) > 0 else 0.0
        # Safety check: if balance seems unreasonably high (>50k), recalculate from unfiltered data
        # This handles cases where cached data might have incorrect values
        if current_balance > 50000:
            # Recalculate from the full dataset, sorted by date
            df_sorted = df.sort_values('Date').reset_index(drop=True)
            current_balance = float(df_sorted['Balance'].iloc[-1]) if len(df_sorted) > 0 else 0.0
        total_income = filtered_df[filtered_df['Amount'] > 0]['Amount'].sum()
        total_expenses = abs(filtered_df[filtered_df['Amount'] < 0]['Amount'].sum())
        date_range_days = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
    else:
        current_balance = 0
        total_income = 0
        total_expenses = 0
        date_range_days = 1
    
    net_flow = total_income - total_expenses
    expenses_df = filtered_df[filtered_df['Amount'] < 0].copy() if len(filtered_df) > 0 else pd.DataFrame()
    income_df = filtered_df[filtered_df['Amount'] > 0].copy() if len(filtered_df) > 0 else pd.DataFrame()
    
    # Date range calculations
    date_range_months = date_range_days / 30.44 if date_range_days > 0 else 1
    
    # Monthly calculations
    # Monthly income is fixed at €1000 (monthly stipend)
    avg_monthly_income = 1000.0
    
    avg_monthly_expenses = total_expenses / max(date_range_months, 1)
    savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
    
    # Budget calculations - use the most recent month in filtered data, not the actual current month
    if len(expenses_df) > 0:
        # Get the most recent month from the filtered data
        expenses_df_sorted = expenses_df.sort_values('Date')
        most_recent_date = expenses_df_sorted['Date'].iloc[-1]
        current_month = most_recent_date.strftime('%Y-%m')
        current_month_expenses = expenses_df[expenses_df['Date'].dt.to_period('M').astype(str) == current_month]['Amount_Abs'].sum()
    else:
        current_month = datetime.now().strftime('%Y-%m')
        current_month_expenses = 0
    budget_used_pct = (current_month_expenses / monthly_budget * 100) if monthly_budget > 0 else 0
    budget_remaining = monthly_budget - current_month_expenses
    
    # Key Metrics - Modern Card Layout
    st.markdown("## FINANCIAL OVERVIEW")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #00f5ff;">
            <div class="metric-label">Current Balance</div>
            <div class="metric-value">€{current_balance:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #00f5ff;">
            <div class="metric-label">Monthly Income</div>
            <div class="metric-value">€{avg_monthly_income:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ff00ff;">
            <div class="metric-label">Monthly Expenses</div>
            <div class="metric-value">€{avg_monthly_expenses:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        net_color = "#00f5ff" if net_flow >= 0 else "#ff00ff"
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {net_color};">
            <div class="metric-label">Net Flow</div>
            <div class="metric-value">€{net_flow:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget Progress & Savings Rate
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Monthly Budget")
        budget_color = "#00f5ff" if budget_used_pct < 80 else "#ffd700" if budget_used_pct < 100 else "#ff00ff"
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #a0a0a0;">Spent this month</span>
                <span style="font-weight: 700; color: {budget_color};">€{current_month_expenses:,.2f} / €{monthly_budget:,.2f}</span>
            </div>
            <div style="height: 12px; background: rgba(255, 255, 255, 0.1); border-radius: 6px; overflow: hidden;">
                <div style="height: 100%; width: {min(budget_used_pct, 100)}%; background: linear-gradient(90deg, {budget_color} 0%, {budget_color}80 100%); transition: width 0.3s;"></div>
            </div>
            <div style="margin-top: 0.5rem; color: #a0a0a0; font-size: 0.875rem;">
                {budget_used_pct:.1f}% used • €{max(budget_remaining, 0):,.2f} remaining
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Savings Rate")
        savings_color = "#00f5ff" if savings_rate >= 20 else "#ffd700" if savings_rate >= 0 else "#ff00ff"
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <div style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, {savings_color} 0%, {savings_color}80 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 1rem 0;">
                {savings_rate:.1f}%
            </div>
            <div style="color: #a0a0a0; font-size: 0.875rem;">
                {'Excellent' if savings_rate >= 20 else 'Good' if savings_rate >= 0 else 'Needs improvement'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dashboard", 
        "Spending Analysis", 
        "Trends", 
        "Locations", 
        "Transactions",
        "Methodology"
    ])
    
    # Weekday mapping for visualizations
    weekday_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 
                   'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    
    # Calculate monthly summary
    if len(filtered_df) > 0:
        monthly_df = filtered_df.copy()
        monthly_df['YearMonth'] = monthly_df['Date'].dt.to_period('M').astype(str)
        income_monthly = monthly_df[monthly_df['Amount'] > 0].groupby('YearMonth')['Amount'].sum().reset_index()
        income_monthly.columns = ['Month', 'Income']
        expenses_monthly = monthly_df[monthly_df['Amount'] < 0].groupby('YearMonth')['Amount_Abs'].sum().reset_index()
        expenses_monthly.columns = ['Month', 'Expenses']
        monthly_summary = pd.merge(income_monthly, expenses_monthly, on='Month', how='outer').fillna(0)
        monthly_summary = monthly_summary.sort_values('Month')
        monthly_summary['Net'] = monthly_summary['Income'] - monthly_summary['Expenses']
    else:
        monthly_summary = pd.DataFrame(columns=['Month', 'Income', 'Expenses', 'Net'])
    
    # Color palette - vibrant neon colors
    colors = {
        'primary': '#00f5ff',
        'secondary': '#ff00ff',
        'accent': '#ffd700',
        'income': '#00f5ff',
        'expense': '#ff00ff',
        'positive': '#00f5ff',
        'negative': '#ff00ff'
    }
    
    # Vibrant color palette for charts
    vibrant_colors = px.colors.qualitative.Vivid + px.colors.qualitative.Set3
    
    with tab1:
        st.markdown("## Financial Dashboard")
        
        # Balance Over Time and Top Categories - Side by Side
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Account Balance Trend")
            if len(filtered_df) > 0:
                balance_df = filtered_df.groupby('Date')['Balance'].last().reset_index().sort_values('Date')
            else:
                balance_df = pd.DataFrame(columns=['Date', 'Balance'])
            if len(balance_df) > 0:
                fig_balance = px.area(
                    balance_df,
                    x='Date',
                    y='Balance',
                    title="",
                    labels={'Balance': 'Balance (€)', 'Date': 'Date'},
                    color_discrete_sequence=[colors['primary']]
                )
                fig_balance.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    hovermode='x unified',
                    height=400,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                fig_balance.add_hline(y=current_balance, line_dash="dash", line_color=colors['secondary'], 
                                     annotation_text=f"Current: €{current_balance:,.0f}")
                st.plotly_chart(fig_balance, use_container_width=True, key="balance_trend")
            else:
                st.info("No data available for the selected filters.")
        
        with col2:
            st.markdown("### Top Spending Categories")
            if len(expenses_df) > 0:
                top_cats = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
                top_cats = top_cats.sort_values('Amount_Abs', ascending=False).head(5)
                top_cats['Percentage'] = (top_cats['Amount_Abs'] / top_cats['Amount_Abs'].sum() * 100).round(1)
                
                fig_categories = px.bar(
                    top_cats,
                    x='Amount_Abs',
                    y='Merchant_Category',
                    orientation='h',
                    title="",
                    labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                    color='Amount_Abs',
                    color_continuous_scale='Plasma',
                    text='Amount_Abs'
                )
                fig_categories.update_traces(
                    texttemplate='€%{text:,.0f}',
                    textposition='outside',
                    textfont_color='#ffffff'
                )
                fig_categories.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=400,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=False, categoryorder='total ascending')
                )
                st.plotly_chart(fig_categories, use_container_width=True, key="top_categories_bar")
            else:
                st.info("No expense data available.")
        
        # Income vs Expenses Chart
        st.markdown("### Income vs Expenses")
        if len(monthly_summary) > 0:
            fig_monthly = go.Figure()
            fig_monthly.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Income'],
                name='Income',
                marker_color=colors['income']
            ))
            fig_monthly.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Expenses'],
                name='Expenses',
                marker_color=colors['expense']
            ))
            fig_monthly.add_trace(go.Scatter(
                x=monthly_summary['Month'],
                y=monthly_summary['Net'],
                name='Net Flow',
                mode='lines+markers',
                line=dict(color=colors['accent'], width=3),
                marker=dict(size=8)
            ))
            fig_monthly.update_layout(
                title="",
                xaxis_title="Month",
                yaxis_title="Amount (€)",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                hovermode='x unified',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#ffffff', size=11)),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_monthly, use_container_width=True, key="income_expenses")
        else:
            st.info("No monthly data available for the selected filters.")
        
        # Expenses by Category - Bar Chart
        st.markdown("### Expenses by Category")
        if len(expenses_df) > 0:
            category_expenses = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
            category_expenses = category_expenses.sort_values('Amount_Abs', ascending=False)
            
            fig_category = px.bar(
                category_expenses,
                x='Merchant_Category',
                y='Amount_Abs',
                title="",
                labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                color='Amount_Abs',
                color_continuous_scale='Plasma',
                text='Amount_Abs'
            )
            fig_category.update_traces(
                texttemplate='€%{text:,.0f}',
                textposition='outside',
                textfont=dict(color='#ffffff', size=12, family='Inter')
            )
            fig_category.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_category, use_container_width=True, key="category_bar_spending_tab")
        
        # Financial Health Gauge
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Financial Health Score")
            if total_income > 0:
                health_score = min(100, max(0, (savings_rate + 50)))
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=health_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Financial Health Score", 'font': {'color': '#ffffff', 'size': 16}},
                    delta={'reference': 50, 'font': {'color': '#ffffff'}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickcolor': '#ffffff'},
                        'bar': {'color': colors['primary']},
                        'steps': [
                            {'range': [0, 33], 'color': 'rgba(255, 0, 255, 0.2)'},
                            {'range': [33, 66], 'color': 'rgba(255, 215, 0, 0.2)'},
                            {'range': [66, 100], 'color': 'rgba(0, 245, 255, 0.2)'}
                        ],
                        'threshold': {
                            'line': {'color': colors['secondary'], 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0)
                    )
                st.plotly_chart(fig_gauge, use_container_width=True, key="gauge_chart")
            
        with col2:
            st.markdown("### Monthly Net Flow Waterfall")
            if len(monthly_summary) > 0:
                waterfall_data = monthly_summary.copy()
                waterfall_data['Net_Flow'] = waterfall_data['Net']
                
                fig_waterfall = go.Figure(go.Waterfall(
                    name="Net Flow",
                    orientation="v",
                    measure=["relative"] * (len(waterfall_data) - 1) + ["total"],
                    x=waterfall_data['Month'],
                    textposition="outside",
                    text=waterfall_data['Net_Flow'].apply(lambda x: f"€{x:,.0f}"),
                    y=waterfall_data['Net_Flow'],
                    connector={"line": {"color": colors['accent']}},
                    increasing={"marker": {"color": colors['income']}},
                    decreasing={"marker": {"color": colors['expense']}},
                    totals={"marker": {"color": colors['accent']}}
                ))
                fig_waterfall.update_layout(
                    title="",
                    xaxis_title="Month",
                    yaxis_title="Net Flow (€)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    showlegend=False,
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_waterfall, use_container_width=True, key="waterfall_chart")
        
        # Advanced Transaction Visualizations
        st.markdown("### Advanced Transaction Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Transaction Size vs Balance")
            if len(filtered_df) > 0:
                scatter_df = filtered_df[filtered_df['Amount'] != 0].copy()
                if len(scatter_df) > 0:
                    scatter_df['Transaction_Type'] = scatter_df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
                    fig_scatter = px.scatter(
                        scatter_df.head(500),
                        x='Amount_Abs',
                        y='Balance',
                        color='Transaction_Type',
                        size='Amount_Abs',
                        hover_data=['Merchant_Category', 'Date'],
                        title="",
                        labels={'Amount_Abs': 'Transaction Amount (€)', 'Balance': 'Account Balance (€)'},
                        color_discrete_map={'Income': colors['income'], 'Expense': colors['expense']}
                    )
                    fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_balance")
        
        with col2:
            st.markdown("#### 3D Scatter: Amount vs Hour vs Day")
            if len(expenses_df) > 0:
                scatter_3d_data = expenses_df.head(300).copy()
                scatter_3d_data['Weekday_Num'] = scatter_3d_data['Weekday'].map(weekday_map)
                
                if len(scatter_3d_data) > 0:
                    fig_3d = px.scatter_3d(
                        scatter_3d_data,
                        x='Hour',
                        y='Weekday_Num',
                        z='Amount_Abs',
                        color='Merchant_Category',
                        size='Amount_Abs',
                        hover_data=['Date'],
                        title="",
                        labels={'Hour': 'Hour of Day', 'Weekday_Num': 'Day of Week', 'Amount_Abs': 'Amount (€)'},
                        color_discrete_sequence=vibrant_colors
                    )
                    fig_3d.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        legend=dict(font=dict(color='#ffffff', size=11)),
                        scene=dict(
                            xaxis_title="Hour",
                            yaxis_title="Day of Week",
                            zaxis_title="Amount (€)",
                            bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)'),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)'),
                            zaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)')
                        )
                    )
                    st.plotly_chart(fig_3d, use_container_width=True, key="3d_scatter")
        
        # Hierarchical Visualizations
        st.markdown("### Hierarchical Views")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Account Type → Category → Transaction Type")
            if len(filtered_df) > 0:
                sunburst_data = filtered_df.groupby(['Product', 'Merchant_Category', 'Type']).size().reset_index(name='Count')
                sunburst_data = sunburst_data[sunburst_data['Count'] > 0]
                
                if len(sunburst_data) > 0:
                    fig_sunburst = px.sunburst(
                        sunburst_data,
                        path=['Product', 'Merchant_Category', 'Type'],
                        values='Count',
                        title="",
                        color='Count',
                        color_continuous_scale='Plasma'
                    )
                    fig_sunburst.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0),
                        legend=dict(font=dict(color='#ffffff', size=11))
                )
                    st.plotly_chart(fig_sunburst, use_container_width=True, key="sunburst_chart")
        
        with col2:
            st.markdown("#### Category Spending Treemap")
            if len(expenses_df) > 0:
                treemap_data = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
                treemap_data = treemap_data.sort_values('Amount_Abs', ascending=False)
                
                if len(treemap_data) > 0:
                    fig_treemap = px.treemap(
                        treemap_data,
                        path=['Merchant_Category'],
                        values='Amount_Abs',
                        title="",
                        color='Amount_Abs',
                        color_continuous_scale='Plasma'
                    )
                    fig_treemap.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_treemap, use_container_width=True, key="treemap_chart")
    
    with tab2:
        st.markdown("## Spending Analysis")
        
        if len(expenses_df) > 0:
            # Key Spending Metrics
            st.markdown("### Spending Overview")
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                total_spending = expenses_df['Amount_Abs'].sum()
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                    <div class="metric-label">Total Spending</div>
                    <div class="metric-value">€{total_spending:,.2f}</div>
            </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                avg_transaction = expenses_df['Amount_Abs'].mean()
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                    <div class="metric-label">Avg Transaction</div>
                    <div class="metric-value">€{avg_transaction:,.2f}</div>
            </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                largest_expense = expenses_df['Amount_Abs'].max()
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                    <div class="metric-label">Largest Expense</div>
                    <div class="metric-value">€{largest_expense:,.2f}</div>
            </div>
                """, unsafe_allow_html=True)
            
            with metric_col4:
                total_transactions = len(expenses_df)
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                    <div class="metric-label">Transactions</div>
                    <div class="metric-value">{total_transactions:,}</div>
            </div>
                """, unsafe_allow_html=True)
    
            # Main Spending Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Spending by Category")
            category_expenses = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
            category_expenses = category_expenses.sort_values('Amount_Abs', ascending=False)
            
            fig_category = px.bar(
                category_expenses,
                x='Merchant_Category',
                y='Amount_Abs',
                title="",
                labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                color='Amount_Abs',
                color_continuous_scale='Plasma',
                text='Amount_Abs'
            )
            fig_category.update_traces(
                texttemplate='€%{text:,.0f}',
                textposition='outside',
                textfont=dict(color='#ffffff', size=11)
            )
            fig_category.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_category, use_container_width=True, key="category_bar_spending")
        
        with col2:
            st.markdown("### Spending by Day of Week")
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_expenses = expenses_df.groupby('Weekday')['Amount_Abs'].sum().reset_index()
            weekday_expenses['Weekday'] = pd.Categorical(weekday_expenses['Weekday'], categories=weekday_order, ordered=True)
            weekday_expenses = weekday_expenses.sort_values('Weekday')
            
            fig_weekday = px.bar(
                weekday_expenses,
                x='Weekday',
                y='Amount_Abs',
                title="",
                labels={'Amount_Abs': 'Spending (€)', 'Weekday': 'Day'},
                color='Amount_Abs',
                color_continuous_scale='Plasma',
                text='Amount_Abs'
            )
            fig_weekday.update_traces(
                texttemplate='€%{text:,.0f}',
                textposition='outside',
                textfont=dict(color='#ffffff', size=11)
            )
            fig_weekday.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_weekday, use_container_width=True, key="weekday_spending")
        
        # Temporal Analysis
        st.markdown("### Temporal Spending Patterns")
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### Spending by Hour of Day")
            hour_expenses = expenses_df.groupby('Hour')['Amount_Abs'].sum().reset_index()
            hour_expenses = hour_expenses.sort_values('Hour')
            
            fig_hour = px.line(
                hour_expenses,
                x='Hour',
                y='Amount_Abs',
                title="",
                labels={'Amount_Abs': 'Spending (€)', 'Hour': 'Hour'},
                color_discrete_sequence=[colors['secondary']],
                markers=True
            )
            fig_hour.update_traces(
                line=dict(width=3),
                marker=dict(size=6),
                fill='tonexty',
                fillcolor=f'rgba(255, 0, 255, 0.1)'
            )
            fig_hour.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                hovermode='x unified',
                height=350,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(tickmode='linear', dtick=2, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_hour, use_container_width=True, key="hour_spending")
        
        with col4:
            st.markdown("#### Spending Heatmap: Day vs Hour")
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = expenses_df.groupby(['Weekday', 'Hour'])['Amount_Abs'].sum().reset_index()
            heatmap_data['Weekday'] = pd.Categorical(heatmap_data['Weekday'], categories=weekday_order, ordered=True)
            heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='Hour', values='Amount_Abs').fillna(0)
            
            fig_heatmap = px.imshow(
                heatmap_pivot,
                labels=dict(x="Hour", y="Day", color="Spending (€)"),
                title="",
                color_continuous_scale='Plasma',
                aspect="auto"
            )
            fig_heatmap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=350,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig_heatmap, use_container_width=True, key="spending_heatmap_spending_tab")
        
        # Top Merchants
        st.markdown("### Top Spending Locations")
        if len(expenses_df) > 0:
            top_merchants = expenses_df.groupby('Description_Anon')['Amount_Abs'].sum().reset_index()
            top_merchants = top_merchants.sort_values('Amount_Abs', ascending=False).head(15)
            top_merchants.columns = ['Merchant', 'Total Spent']
            
            fig_merchants = px.bar(
                top_merchants,
                x='Total Spent',
                y='Merchant',
                orientation='h',
                title="",
                labels={'Total Spent': 'Total Spent (€)', 'Merchant': 'Merchant'},
                color='Total Spent',
                color_continuous_scale='Plasma',
                text='Total Spent'
            )
            fig_merchants.update_traces(
                texttemplate='€%{text:,.0f}',
                textposition='outside',
                textfont=dict(color='#ffffff', size=10)
            )
            fig_merchants.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=450,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_merchants, use_container_width=True, key="top_merchants")
        
        # Additional Spending Insights
        st.markdown("### Spending Insights")
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown("#### Monthly Spending by Category")
            if len(expenses_df) > 0 and 'Date' in expenses_df.columns:
                expenses_df_copy = expenses_df.copy()
                expenses_df_copy['YearMonth'] = expenses_df_copy['Date'].dt.to_period('M').astype(str)
                top_cats_monthly = expenses_df_copy.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(5).index
                monthly_cat = expenses_df_copy[expenses_df_copy['Merchant_Category'].isin(top_cats_monthly)]
                monthly_cat_summary = monthly_cat.groupby(['YearMonth', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                
                if len(monthly_cat_summary) > 0:
                    fig_monthly_cat = px.line(
                        monthly_cat_summary,
                        x='YearMonth',
                        y='Amount_Abs',
                        color='Merchant_Category',
                        title="",
                        labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                        markers=True,
                        color_discrete_sequence=vibrant_colors
                    )
                    fig_monthly_cat.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        hovermode='x unified',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_monthly_cat, use_container_width=True, key="monthly_category_trends")
        
        with col6:
            st.markdown("#### Average Spending per Transaction by Category")
            if len(expenses_df) > 0:
                avg_by_category = expenses_df.groupby('Merchant_Category').agg({
                    'Amount_Abs': ['mean', 'count']
                }).reset_index()
                avg_by_category.columns = ['Category', 'Avg_Amount', 'Count']
                avg_by_category = avg_by_category[avg_by_category['Count'] >= 3]  # Only categories with at least 3 transactions
                avg_by_category = avg_by_category.sort_values('Avg_Amount', ascending=False).head(8)
                
                fig_avg_cat = px.bar(
                    avg_by_category,
                    x='Category',
                    y='Avg_Amount',
                    title="",
                    labels={'Avg_Amount': 'Average Amount (€)', 'Category': 'Category'},
                    color='Avg_Amount',
                    color_continuous_scale='Plasma',
                    text='Avg_Amount'
                )
                fig_avg_cat.update_traces(
                    texttemplate='€%{text:,.0f}',
                    textposition='outside',
                    textfont=dict(color='#ffffff', size=10)
                )
                fig_avg_cat.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_avg_cat, use_container_width=True, key="avg_category_spending")
        
        # Advanced Spending Visualizations
        st.markdown("### Spending Distribution Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Transaction Amount Distribution by Category")
            if len(expenses_df) > 0:
                top_cats = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(8).index
                expenses_filtered = expenses_df[expenses_df['Merchant_Category'].isin(top_cats)]
                
                if len(expenses_filtered) > 0:
                    fig_box = px.box(
                        expenses_filtered,
                        x='Merchant_Category',
                        y='Amount_Abs',
                        title="",
                        labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                        color='Merchant_Category',
                        color_discrete_sequence=vibrant_colors
                    )
                    fig_box.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        xaxis_tickangle=-45,
                        showlegend=False,
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_box, use_container_width=True, key="box_plot_categories")
        
        with col2:
            st.markdown("#### Spending Distribution (Violin Plot)")
            if len(expenses_df) > 0:
                top_cats_violin = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(6).index
                expenses_violin = expenses_df[expenses_df['Merchant_Category'].isin(top_cats_violin)]
                
                if len(expenses_violin) > 0:
                    fig_violin = px.violin(
                        expenses_violin,
                        x='Merchant_Category',
                        y='Amount_Abs',
                        title="",
                        labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                        color='Merchant_Category',
                        color_discrete_sequence=vibrant_colors,
                        box=True
                    )
                    fig_violin.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        xaxis_tickangle=-45,
                        showlegend=False,
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_violin, use_container_width=True, key="violin_plot")
        
    
    with tab3:
        st.markdown("## Trends & Analytics")
        
        # Key Insights - Moved to top
        st.markdown("### Key Insights")
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            if len(expenses_df) > 0:
                top_category = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().idxmax()
                top_category_amount = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().max()
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 0.875rem; color: #a0a0a0; margin-bottom: 0.5rem;">Top Spending Category</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">{top_category}</div>
                    <div style="font-size: 1rem; color: {colors['primary']}; margin-top: 0.5rem;">€{top_category_amount:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with insight_col2:
            if len(expenses_df) > 0:
                peak_hour = expenses_df.groupby('Hour')['Amount_Abs'].sum().idxmax()
                peak_hour_amount = expenses_df.groupby('Hour')['Amount_Abs'].sum().max()
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 0.875rem; color: #a0a0a0; margin-bottom: 0.5rem;">Peak Spending Hour</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">{peak_hour}:00</div>
                    <div style="font-size: 1rem; color: {colors['primary']}; margin-top: 0.5rem;">€{peak_hour_amount:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with insight_col3:
            if len(expenses_df) > 0:
                avg_expense = expenses_df['Amount_Abs'].mean()
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 0.875rem; color: #a0a0a0; margin-bottom: 0.5rem;">Average Transaction</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">€{avg_expense:,.2f}</div>
                    <div style="font-size: 1rem; color: {colors['primary']}; margin-top: 0.5rem;">per transaction</div>
                </div>
                """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Category Trends Over Time")
            if len(expenses_df) > 0 and 'Date' in expenses_df.columns:
                top_categories = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(5).index
                category_trends = expenses_df[expenses_df['Merchant_Category'].isin(top_categories)].copy()
                if len(category_trends) > 0:
                    category_trends['YearMonth'] = category_trends['Date'].dt.to_period('M').astype(str)
                    category_monthly = category_trends.groupby(['YearMonth', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                else:
                    category_monthly = pd.DataFrame(columns=['YearMonth', 'Merchant_Category', 'Amount_Abs'])
            else:
                category_monthly = pd.DataFrame(columns=['YearMonth', 'Merchant_Category', 'Amount_Abs'])
            
            if len(category_monthly) > 0:
                fig_trends = px.line(
                    category_monthly,
                    x='YearMonth',
                    y='Amount_Abs',
                    color='Merchant_Category',
                    title="",
                    labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                    markers=True,
                    color_discrete_sequence=vibrant_colors
                )
                fig_trends.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    hovermode='x unified',
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    legend=dict(font=dict(color='#ffffff', size=11))
                )
                st.plotly_chart(fig_trends, use_container_width=True, key="category_trends")
            else:
                st.info("No trend data available.")
        
        with col2:
            st.markdown("### Spending Heatmap: Day vs Hour")
            if len(expenses_df) > 0:
                weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                heatmap_data = expenses_df.groupby(['Weekday', 'Hour'])['Amount_Abs'].sum().reset_index()
                heatmap_data['Weekday'] = pd.Categorical(heatmap_data['Weekday'], categories=weekday_order, ordered=True)
                heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='Hour', values='Amount_Abs').fillna(0)
                
                fig_heatmap = px.imshow(
                    heatmap_pivot,
                    labels=dict(x="Hour", y="Day", color="Spending (€)"),
                    title="",
                    color_continuous_scale='Plasma',
                    aspect="auto"
                )
                fig_heatmap.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig_heatmap, use_container_width=True, key="spending_heatmap_trends_tab")
        
        # Cumulative Spending
        st.markdown("### Cumulative Spending Over Time")
        if len(expenses_df) > 0 and 'Date' in expenses_df.columns:
            expenses_sorted = expenses_df.sort_values('Date').copy()
            expenses_sorted['Cumulative'] = expenses_sorted['Amount_Abs'].cumsum()
            
            fig_cumulative = px.line(
                expenses_sorted,
                x='Date',
                y='Cumulative',
                title="",
                labels={'Cumulative': 'Cumulative Spending (€)', 'Date': 'Date'},
                color_discrete_sequence=[colors['expense']]
            )
            fig_cumulative.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                hovermode='x unified',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_cumulative, use_container_width=True, key="cumulative_spending")
        
        # Advanced Trend Visualizations
        st.markdown("### Advanced Trend Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stacked Area: Category Trends")
            if len(expenses_df) > 0 and 'Date' in expenses_df.columns:
                expenses_df_copy = expenses_df.copy()
                expenses_df_copy['YearMonth'] = expenses_df_copy['Date'].dt.to_period('M').astype(str)
                top_cats_area = expenses_df_copy.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(6).index
                area_data = expenses_df_copy[expenses_df_copy['Merchant_Category'].isin(top_cats_area)]
                
                if len(area_data) > 0:
                    area_monthly = area_data.groupby(['YearMonth', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                    
                    fig_area = px.area(
                        area_monthly,
                        x='YearMonth',
                        y='Amount_Abs',
                        color='Merchant_Category',
                        title="",
                        labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                        color_discrete_sequence=vibrant_colors
                    )
                    fig_area.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_area, use_container_width=True, key="stacked_area")
        
        with col2:
            st.markdown("#### Spending Pattern Radar Chart")
            if len(expenses_df) > 0:
                weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_spending = expenses_df.groupby('Weekday')['Amount_Abs'].sum().reset_index()
                
                all_weekdays_df = pd.DataFrame({'Weekday': weekday_order})
                weekday_spending = pd.merge(all_weekdays_df, weekday_spending, on='Weekday', how='left')
                weekday_spending['Amount_Abs'] = weekday_spending['Amount_Abs'].fillna(0)
                weekday_spending['Weekday'] = pd.Categorical(weekday_spending['Weekday'], categories=weekday_order, ordered=True)
                weekday_spending = weekday_spending.sort_values('Weekday')
                
                max_val = weekday_spending['Amount_Abs'].max()
                if max_val > 0:
                    weekday_spending['Normalized'] = (weekday_spending['Amount_Abs'] / max_val * 100)
                else:
                    weekday_spending['Normalized'] = 0
                
                # Prepare data for radar chart - need to close the shape by repeating first value
                r_values = weekday_spending['Normalized'].tolist()
                theta_values = weekday_spending['Weekday'].tolist()
                
                # Close the shape by adding the first value at the end
                if len(r_values) > 0:
                    r_values.append(r_values[0])
                    theta_values.append(theta_values[0])
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=r_values,
                    theta=theta_values,
                    fill='toself',
                    name='Spending Pattern',
                    line_color=colors['primary'],
                    fillcolor=colors['primary'],
                    opacity=0.3
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickcolor='#ffffff',
                            tickfont=dict(color='#ffffff', size=10),
                            gridcolor='rgba(255,255,255,0.2)',
                            linecolor='rgba(255,255,255,0.3)',
                            showline=True
                        ),
                        angularaxis=dict(
                            tickcolor='#ffffff',
                            tickfont=dict(color='#ffffff', size=10),
                            gridcolor='rgba(255,255,255,0.2)',
                            linecolor='rgba(255,255,255,0.3)',
                            showline=True
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    showlegend=True,
                    title="",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    legend=dict(font=dict(color='#ffffff', size=11))
                )
                st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")
        
        # Multi-dimensional Analysis
        st.markdown("### Multi-Dimensional Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Parallel Coordinates")
            if len(expenses_df) > 0:
                parallel_data = expenses_df[['Amount_Abs', 'Hour', 'Weekday', 'Merchant_Category']].copy()
                parallel_data = parallel_data.head(200)
                
                parallel_data['Weekday_Num'] = parallel_data['Weekday'].map(weekday_map)
                
                top_cats_parallel = parallel_data['Merchant_Category'].value_counts().head(5).index
                parallel_data = parallel_data[parallel_data['Merchant_Category'].isin(top_cats_parallel)]
                
                if len(parallel_data) > 0:
                    fig_parallel = px.parallel_coordinates(
                        parallel_data,
                        color='Amount_Abs',
                        dimensions=['Amount_Abs', 'Hour', 'Weekday_Num'],
                        labels={'Amount_Abs': 'Amount', 'Hour': 'Hour', 'Weekday_Num': 'Day'},
                        color_continuous_scale='Plasma',
                        title=""
                    )
                    fig_parallel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    st.plotly_chart(fig_parallel, use_container_width=True, key="parallel_coords")
        
        with col2:
            st.markdown("#### Transaction Type Funnel")
            if len(filtered_df) > 0:
                funnel_data = {
                    'Stage': ['Total Transactions', 'Card Payments', 'Transfers', 'Topups', 'Other'],
                    'Count': [
                        len(filtered_df),
                        len(filtered_df[filtered_df['Type'] == 'Card Payment']),
                        len(filtered_df[filtered_df['Type'] == 'Transfer']),
                        len(filtered_df[filtered_df['Type'] == 'Topup']),
                        len(filtered_df[~filtered_df['Type'].isin(['Card Payment', 'Transfer', 'Topup'])])
                    ]
                }
                funnel_df = pd.DataFrame(funnel_data)
                fig_funnel = px.funnel(
                    funnel_df,
                    x='Count',
                    y='Stage',
                    title="",
                    labels={'Count': 'Number of Transactions', 'Stage': 'Transaction Type'}
                )
                fig_funnel.update_traces(marker_color=colors['primary'])
                fig_funnel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_funnel, use_container_width=True, key="funnel_chart")
    
    with tab4:
        st.markdown("## Location-Based Spending Analysis")
        
        if 'Country' in filtered_df.columns and filtered_df['Country'].nunique() > 1:
            # Location Overview Metrics
            st.markdown("### Location Overview")
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_metrics = expenses_df.groupby('Country').agg({
                    'Amount_Abs': ['sum', 'mean', 'count']
                }).reset_index()
                country_metrics.columns = ['Country', 'Total_Spending', 'Avg_Transaction', 'Transaction_Count']
                country_metrics = country_metrics.sort_values('Total_Spending', ascending=False)
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    total_countries = len(country_metrics)
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #00f5ff;">
                        <div class="metric-label">Countries Visited</div>
                        <div class="metric-value">{total_countries}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    top_country = country_metrics.iloc[0]['Country'] if len(country_metrics) > 0 else 'N/A'
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #00f5ff;">
                        <div class="metric-label">Top Country</div>
                        <div class="metric-value" style="font-size: 1.5rem;">{top_country}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    top_spending = country_metrics.iloc[0]['Total_Spending'] if len(country_metrics) > 0 else 0
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                        <div class="metric-label">Highest Spending</div>
                        <div class="metric-value">€{top_spending:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col4:
                    avg_per_country = country_metrics['Total_Spending'].mean() if len(country_metrics) > 0 else 0
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                        <div class="metric-label">Avg per Country</div>
                        <div class="metric-value">€{avg_per_country:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # World Map Visualization
            st.markdown("### World Map: Spending by Country")
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_spending_map = expenses_df.groupby('Country')['Amount_Abs'].sum().reset_index()
                country_spending_map.columns = ['Country', 'Spending']
                
                # Country name to ISO code mapping (common countries)
                country_to_iso = {
                    'France': 'FRA',
                    'United States': 'USA',
                    'United Kingdom': 'GBR',
                    'Germany': 'DEU',
                    'Spain': 'ESP',
                    'Italy': 'ITA',
                    'Netherlands': 'NLD',
                    'Belgium': 'BEL',
                    'Switzerland': 'CHE',
                    'Portugal': 'PRT',
                    'Austria': 'AUT',
                    'Poland': 'POL',
                    'Sweden': 'SWE',
                    'Denmark': 'DNK',
                    'Norway': 'NOR',
                    'Finland': 'FIN',
                    'Ireland': 'IRL',
                    'Greece': 'GRC',
                    'Czech Republic': 'CZE',
                    'Romania': 'ROU',
                    'Hungary': 'HUN',
                    'Canada': 'CAN',
                    'Australia': 'AUS',
                    'Japan': 'JPN',
                    'China': 'CHN',
                    'India': 'IND',
                    'Brazil': 'BRA',
                    'Mexico': 'MEX',
                    'Argentina': 'ARG',
                    'South Korea': 'KOR',
                    'Singapore': 'SGP',
                    'Thailand': 'THA',
                    'Indonesia': 'IDN',
                    'Malaysia': 'MYS',
                    'Philippines': 'PHL',
                    'Vietnam': 'VNM',
                    'New Zealand': 'NZL',
                    'South Africa': 'ZAF',
                    'Turkey': 'TUR',
                    'Israel': 'ISR',
                    'United Arab Emirates': 'ARE',
                    'Saudi Arabia': 'SAU',
                    'Egypt': 'EGY',
                    'Morocco': 'MAR',
                    'Tunisia': 'TUN',
                    'Algeria': 'DZA',
                    'Russia': 'RUS',
                    'Ukraine': 'UKR',
                    'Croatia': 'HRV',
                    'Serbia': 'SRB',
                    'Bulgaria': 'BGR',
                    'Slovakia': 'SVK',
                    'Slovenia': 'SVN',
                    'Estonia': 'EST',
                    'Latvia': 'LVA',
                    'Lithuania': 'LTU',
                    'Luxembourg': 'LUX',
                    'Iceland': 'ISL',
                    'Cyprus': 'CYP',
                    'Malta': 'MLT'
                }
                
                # Add ISO codes
                country_spending_map['ISO'] = country_spending_map['Country'].map(country_to_iso)
                country_spending_map = country_spending_map.dropna(subset=['ISO'])
                
                if len(country_spending_map) > 0:
                    fig_map = px.choropleth(
                        country_spending_map,
                        locations='ISO',
                        color='Spending',
                        hover_name='Country',
                        hover_data={'ISO': False, 'Spending': ':,.2f'},
                        color_continuous_scale='Plasma',
                        title="",
                        labels={'Spending': 'Spending (€)'}
                    )
                    fig_map.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        geo=dict(
                            bgcolor='rgba(0,0,0,0)',
                            lakecolor='rgba(0,0,0,0)',
                            landcolor='rgba(255,255,255,0.1)',
                            showlakes=False,
                            showland=True,
                            showocean=True,
                            oceancolor='rgba(0,0,0,0.3)',
                            projection_type='natural earth'
                        ),
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    fig_map.update_geos(
                        showcountries=True,
                        countrycolor='rgba(255,255,255,0.3)',
                        showcoastlines=True,
                        coastlinecolor='rgba(255,255,255,0.2)'
                    )
                    st.plotly_chart(fig_map, use_container_width=True, key="world_map")
                else:
                    st.info("Country data not available in ISO format for world map visualization.")
            
            # Country Comparison
            st.markdown("### Country Comparison")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Total Spending by Country")
                if len(expenses_df) > 0:
                    country_spending = expenses_df.groupby('Country')['Amount_Abs'].sum().reset_index()
                    country_spending = country_spending.sort_values('Amount_Abs', ascending=False)
                    
                    fig_country = px.bar(
                        country_spending,
                        x='Country',
                        y='Amount_Abs',
                        title="",
                        labels={'Amount_Abs': 'Spending (€)', 'Country': 'Country'},
                        color='Amount_Abs',
                        color_continuous_scale='Plasma',
                        text='Amount_Abs'
                    )
                    fig_country.update_traces(
                        texttemplate='€%{text:,.0f}',
                        textposition='outside',
                        textfont=dict(color='#ffffff', size=11)
                    )
                    fig_country.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        showlegend=False,
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_country, use_container_width=True, key="country_bar")
        
            with col2:
                st.markdown("#### Average Transaction by Country")
                if len(expenses_df) > 0:
                    country_avg = expenses_df.groupby('Country').agg({
                        'Amount_Abs': ['mean', 'count']
                    }).reset_index()
                    country_avg.columns = ['Country', 'Avg_Amount', 'Count']
                    country_avg = country_avg[country_avg['Count'] >= 3]  # At least 3 transactions
                    country_avg = country_avg.sort_values('Avg_Amount', ascending=False)
                    
                    fig_avg = px.bar(
                        country_avg,
                        x='Country',
                        y='Avg_Amount',
                        title="",
                        labels={'Avg_Amount': 'Average Amount (€)', 'Country': 'Country'},
                        color='Avg_Amount',
                        color_continuous_scale='Plasma',
                        text='Avg_Amount'
                    )
                    fig_avg.update_traces(
                        texttemplate='€%{text:,.0f}',
                        textposition='outside',
                        textfont=dict(color='#ffffff', size=11)
                    )
                    fig_avg.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        showlegend=False,
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_avg, use_container_width=True, key="country_avg")
            
            # Monthly trends by country
            st.markdown("### Monthly Spending Trends by Country")
            if len(expenses_df) > 0 and 'Date' in expenses_df.columns and 'Country' in expenses_df.columns:
                expenses_df_copy = expenses_df.copy()
                expenses_df_copy['YearMonth'] = expenses_df_copy['Date'].dt.to_period('M').astype(str)
                country_monthly = expenses_df_copy.groupby(['YearMonth', 'Country'])['Amount_Abs'].sum().reset_index()
                
                if len(country_monthly) > 0:
                    fig_country_trend = px.line(
                        country_monthly,
                        x='YearMonth',
                        y='Amount_Abs',
                        color='Country',
                        title="",
                        labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                        markers=True,
                        color_discrete_sequence=vibrant_colors
                    )
                    fig_country_trend.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        hovermode='x unified',
                        height=450,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_country_trend, use_container_width=True, key="country_trends")
                else:
                    st.info("No country trend data available.")
            
            # City Analysis
            if 'City' in expenses_df.columns and expenses_df['City'].nunique() > 1:
                st.markdown("### City-Level Analysis")
                col3, col4 = st.columns(2)
                
                with col3:
                    st.markdown("#### Spending by City")
                    city_spending = expenses_df.groupby('City')['Amount_Abs'].sum().reset_index()
                    city_spending = city_spending.sort_values('Amount_Abs', ascending=False).head(10)
                    
                    fig_city = px.bar(
                        city_spending,
                        x='City',
                        y='Amount_Abs',
                        title="",
                        labels={'Amount_Abs': 'Spending (€)', 'City': 'City'},
                        color='Amount_Abs',
                        color_continuous_scale='Plasma',
                        text='Amount_Abs'
                    )
                    fig_city.update_traces(
                        texttemplate='€%{text:,.0f}',
                        textposition='outside',
                        textfont=dict(color='#ffffff', size=10)
                    )
                    fig_city.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        showlegend=False,
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_city, use_container_width=True, key="city_bar")
                
                with col4:
                    st.markdown("#### Category Spending by Country")
        if len(expenses_df) > 0:
                        heatmap_country = expenses_df.groupby(['Country', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                        heatmap_pivot = heatmap_country.pivot(index='Merchant_Category', columns='Country', values='Amount_Abs').fillna(0)
                        
                        if len(heatmap_pivot) > 0:
                            fig_heatmap_country = px.imshow(
                                heatmap_pivot,
                                labels=dict(x="Country", y="Category", color="Spending (€)"),
                                title="",
                                color_continuous_scale='Plasma',
                                aspect="auto"
                            )
                            fig_heatmap_country.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#ffffff',
                                height=400,
                                margin=dict(l=0, r=0, t=0, b=0)
                            )
                            st.plotly_chart(fig_heatmap_country, use_container_width=True, key="heatmap_country_category")
        else:
            st.info("Location data not available for the selected filters.")
    
    with tab5:
        st.markdown("## Transaction Details")
        
        search_term = st.text_input("Search transactions", placeholder="Search by merchant, category, or description...")
        
        display_df = filtered_df.copy()
        if search_term and len(display_df) > 0:
            if 'Description_Anon' in display_df.columns and 'Merchant_Category' in display_df.columns:
                display_df = display_df[
                    display_df['Description_Anon'].str.contains(search_term, case=False, na=False) |
                    display_df['Merchant_Category'].str.contains(search_term, case=False, na=False)
                ]
        
        if len(display_df) > 0:
            required_cols = ['Date', 'Type', 'Merchant_Category', 'Description_Anon', 'Amount', 'Balance']
            available_cols = [col for col in required_cols if col in display_df.columns]
            
            if len(available_cols) > 0:
                display_df = display_df[available_cols].copy()
                if 'Date' in display_df.columns:
                    display_df = display_df.sort_values('Date', ascending=False)
                    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
                if 'Amount' in display_df.columns:
                    display_df['Amount'] = display_df['Amount'].apply(lambda x: f"€{float(x):,.2f}" if pd.notna(x) else "€0.00")
                if 'Balance' in display_df.columns:
                    display_df['Balance'] = display_df['Balance'].apply(lambda x: f"€{float(x):,.2f}" if pd.notna(x) else "€0.00")
                
                    st.dataframe(
                    display_df,
                        use_container_width=True,
                    hide_index=True,
                    height=600
                )
                
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Data",
                    data=csv,
                    file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No transaction data available.")
        else:
            st.info("No transactions found matching your search criteria.")
    
    with tab6:
        st.markdown("## Methodology & Design")
        
        # Overview
        st.markdown("""
        ### Project Overview
        
        This interactive financial analytics dashboard transforms transaction data into actionable insights, enabling users 
        to understand spending patterns, track financial health, and make informed decisions. Designed for individuals 
        managing personal finances, particularly useful for students and professionals tracking expenses across multiple 
        locations and time periods.
        """)
        
        # Research Questions
        st.markdown("### Research Questions")
        
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            st.markdown("""
            **1. Financial Status**
            - Current balance with trend visualization
            - Income vs expenses (monthly breakdown)
            - Savings rate and health scoring
            - Budget adherence monitoring
            
            **2. Spending Patterns**
            - Category-wise distribution
            - Temporal patterns (hourly, daily, weekly)
            - Peak spending times
            - Merchant-level analysis
            """)
        
        with col_q2:
            st.markdown("""
            **3. Geographic Insights**
            - Country and city-level comparison
            - Cost of living variations
            - World map visualization
            
            **4. Temporal Trends**
            - Monthly evolution
            - Category trends over time
            - Seasonal patterns
            - Cumulative tracking
            """)
        
        # Design & Implementation
        st.markdown("### Design & Implementation")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("""
            **Visual Design**
            
            - **Dark Theme**: Modern aesthetic, reduces eye strain
            - **Color Coding**: Cyan for income, Magenta for expenses (financial conventions)
            - **Chart Selection**: Area charts for trends, bars for comparisons, heatmaps for patterns
            - **Layout**: Wide layout with tabbed interface and persistent sidebar filters
            
            **Data Structure**
            
            - **Temporal**: Date, Year, Month, Day, Weekday, Hour
            - **Financial**: Amount, Balance, Amount_Abs
            - **Categorical**: Type, Product, Merchant_Category
            - **Geographic**: Country, City
            """)
        
        with col_d2:
            st.markdown("""
            **Technology Stack**
            
            - **Streamlit**: Web framework for rapid development
            - **Plotly**: Interactive visualizations
            - **Pandas**: Data manipulation
            - **Python**: Core language
            
            **Key Features**
            
            - Multi-level filtering (date, year, type, category)
            - Real-time visualization updates
            - Interactive charts (zoom, pan, hover)
            - CSV export functionality
            - Data caching for performance
            """)
        
        # Advanced Visualizations
        st.markdown("### Advanced Visualizations")
        
        st.markdown("""
        **Multi-Dimensional**: 3D scatter plots, parallel coordinates, hierarchical sunburst charts, treemaps
        
        **Statistical**: Box plots, violin plots, histograms, waterfall charts
        
        **Geographic**: Choropleth world maps, country/city comparisons, location heatmaps
        """)
        
        # Use Cases & Limitations
        st.markdown("### Use Cases & Limitations")
        
        col_u1, col_u2 = st.columns(2)
        
        with col_u1:
            st.markdown("""
            **Key Use Cases**
            
            - Track financial health (balance, savings rate, budget)
            - Identify spending patterns (when, where, what)
            - Analyze geographic spending variations
            - Monitor trends over time
            - Discover peak spending times
            """)
        
        with col_u2:
            st.markdown("""
            **Current Limitations**
            
            - Transaction-level data only (no investments/assets)
            - Manual CSV import (no API integration)
            - Single monthly budget (no category budgets)
            - No forecasting capabilities
            - Location data may be incomplete
            """)
        
        # Methodology Summary
        st.markdown("### Methodology Summary")
        
        st.markdown("""
        This dashboard follows a **data-driven, user-centered design approach** combining statistical analysis with 
        visual analytics. The methodology emphasizes **exploratory data analysis** where users can formulate questions, 
        explore data through multiple visualizations, discover patterns, and make informed financial decisions.
        
        **Design Principles**: Clarity over complexity, user-centric design, data-driven insights, accessibility, and performance optimization.
        """)

else:
    st.error("Unable to load data. Please check if the data file exists.")
