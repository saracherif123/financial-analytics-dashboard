import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import os
import streamlit.components.v1 as components

# Try to import Google Generative AI (optional - falls back to rule-based if not available)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

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
    /* Hide Streamlit's menu, footer, and header */
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {display: none !important; visibility: hidden !important;}
    header {display: none !important; visibility: hidden !important; height: 0 !important;}
    [data-testid="stHeader"] {display: none !important; visibility: hidden !important; height: 0 !important;}
    .stApp > header {display: none !important; visibility: hidden !important; height: 0 !important;}
    section[data-testid="stHeader"] {display: none !important; visibility: hidden !important; height: 0 !important;}
    
    /* Ensure custom toggle button is ALWAYS visible - Safari compatible */
    #custom-sidebar-toggle-btn {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 999999 !important;
        width: 50px !important;
        height: 50px !important;
        background: rgba(0, 245, 255, 0.9) !important;
        border: 3px solid #00f5ff !important;
        border-radius: 8px !important;
        -webkit-border-radius: 8px !important;
        color: #fff !important;
        font-size: 28px !important;
        cursor: pointer !important;
        -webkit-cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.6) !important;
        -webkit-box-shadow: 0 4px 20px rgba(0, 245, 255, 0.6) !important;
        align-items: center !important;
        justify-content: center !important;
        pointer-events: auto !important;
        -webkit-appearance: none !important;
        -webkit-tap-highlight-color: transparent !important;
    }
    
    /* Ensure sidebar toggle button is ALWAYS visible and clickable - for collapsed sidebar */
    [data-testid="collapsedControl"],
    button[data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        z-index: 99999 !important;
        position: relative !important;
        background: rgba(0, 245, 255, 0.3) !important;
        border: 2px solid #00f5ff !important;
        border-radius: 6px !important;
        padding: 0.4rem !important;
        cursor: pointer !important;
        min-width: 36px !important;
        min-height: 36px !important;
        margin: 0.5rem !important;
        pointer-events: auto !important;
    }
    
    /* Toggle button when sidebar is expanded - different selector */
    [data-testid="stSidebar"] button,
    header button,
    [data-testid="stHeader"] button,
    button[aria-label*="Close"],
    button[aria-label*="Open"],
    button[aria-label*="sidebar"],
    button[aria-label*="menu"] {
        display: block !important;
        visibility: visible !important;
        z-index: 99999 !important;
        background: rgba(0, 245, 255, 0.3) !important;
        border: 2px solid #00f5ff !important;
        border-radius: 6px !important;
        padding: 0.4rem !important;
        cursor: pointer !important;
        min-width: 36px !important;
        min-height: 36px !important;
        pointer-events: auto !important;
    }
    
    [data-testid="collapsedControl"]:hover,
    header button:hover,
    [data-testid="stHeader"] button:hover {
        background: rgba(0, 245, 255, 0.5) !important;
    }
    
    /* Make sure toggle button SVG/icon is visible */
    [data-testid="collapsedControl"] svg,
    header button svg,
    [data-testid="stHeader"] button svg {
        display: block !important;
        visibility: visible !important;
        color: #00f5ff !important;
        fill: #00f5ff !important;
        stroke: #00f5ff !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    [data-testid="collapsedControl"] svg *,
    header button svg *,
    [data-testid="stHeader"] button svg * {
        fill: #00f5ff !important;
        stroke: #00f5ff !important;
    }
    
    /* CRITICAL: Sidebar always visible - works in both Chrome and Safari */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        background: rgba(15, 12, 41, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        transition: transform 0.3s ease !important;
        -webkit-transition: -webkit-transform 0.3s ease !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        z-index: 999 !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        transform: translateX(0) !important;
        -webkit-transform: translateX(0) !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Default state - always visible unless explicitly collapsed */
    [data-testid="stSidebar"]:not([aria-expanded="false"]),
    section[data-testid="stSidebar"]:not([aria-expanded="false"]),
    [data-testid="stSidebar"][aria-expanded="true"],
    section[data-testid="stSidebar"][aria-expanded="true"],
    [data-testid="stSidebar"][aria-expanded=""],
    section[data-testid="stSidebar"][aria-expanded=""] {
        transform: translateX(0) !important;
        -webkit-transform: translateX(0) !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Collapsed state - only when explicitly false */
    [data-testid="stSidebar"][aria-expanded="false"],
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%) !important;
        -webkit-transform: translateX(-100%) !important;
    }
    
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove top decoration */
    .decoration {
        display: none !important;
    }
    
    /* Ensure main content starts at top - sidebar overlays, doesn't push */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: -2rem !important;
        max-width: 100% !important;
        margin-left: 0 !important;
    }
    
    /* Remove top margin from main content */
    [data-testid="stAppViewContainer"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing from first element */
    .main .block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove all top spacing from Streamlit elements */
    [data-testid="stMarkdownContainer"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing from element containers */
    .element-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove top spacing from first markdown */
    .main .block-container [data-testid="stMarkdownContainer"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Aggressively remove all top spacing */
    .main .block-container > div:first-child > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing from vertical blocks */
    [data-testid="stVerticalBlock"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Target the very first element */
    .main .block-container > div:first-child > div:first-child > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove any default Streamlit spacing */
    section[data-testid="stAppViewContainer"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Sidebar visibility already handled above - remove duplicates */
    
    /* Sidebar toggle button always visible */
    [data-testid="stSidebar"] [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"],
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        z-index: 9999 !important;
    }
    
    /* Make sure sidebar toggle button is visible */
    section[data-testid="stSidebar"] button {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Ensure sidebar content is visible */
    [data-testid="stSidebar"] > div {
        visibility: visible !important;
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
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
        line-height: 1.1 !important;
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 0.95rem;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        font-weight: 300;
        line-height: 1.2 !important;
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.2);
        border-color: rgba(0, 245, 255, 0.3);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.5rem 0 0.25rem 0;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.7rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    /* Section Headers */
    h2 {
        color: #00f5ff;
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }
    
    h3 {
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 0.25rem;
        margin-bottom: 0.1rem;
    }
    
    h4 {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.25rem;
        margin-bottom: 0.1rem;
    }
    
    /* Reduce spacing in markdown sections */
    .element-container {
        margin-bottom: 0.1rem !important;
        padding-bottom: 0 !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.1rem !important;
        margin-top: 0.1rem !important;
    }
    
    .stMarkdown p {
        margin-bottom: 0.1rem !important;
        margin-top: 0.1rem !important;
    }
    
    /* Reduce chart margins */
    [data-testid="stPlotlyChart"] {
        margin-top: 0.1rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    
    /* Reduce column gaps */
    [data-testid="column"] {
        gap: 0.5rem !important;
    }
    
    /* Reduce all block spacing */
    [data-testid="stVerticalBlock"] > [data-testid="element-container"] {
        margin-bottom: 0.25rem !important;
    }
    
    /* Sidebar - Proper styling and positioning */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        backdrop-filter: blur(10px);
        visibility: visible !important;
        display: block !important;
        transform: translateX(0) !important;
        opacity: 1 !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
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
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: 100vh !important;
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
    # Inject JavaScript to create custom sidebar toggle button - MUST execute
    # Use components.v1.html to force sidebar visible and create toggle button
    import streamlit.components.v1 as components
    components.html("""
    <script>
    function ensureSidebarVisible() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            // Force sidebar to be visible - works in both browsers
            sidebar.style.setProperty('visibility', 'visible', 'important');
            sidebar.style.setProperty('display', 'block', 'important');
            sidebar.style.setProperty('opacity', '1', 'important');
            sidebar.style.setProperty('position', 'fixed', 'important');
            sidebar.style.setProperty('left', '0', 'important');
            sidebar.style.setProperty('top', '0', 'important');
            sidebar.style.setProperty('height', '100vh', 'important');
            sidebar.style.setProperty('width', '21rem', 'important');
            sidebar.style.setProperty('min-width', '21rem', 'important');
            sidebar.style.setProperty('z-index', '999', 'important');
            sidebar.style.setProperty('background', 'rgba(15, 12, 41, 0.95)', 'important');
            sidebar.style.setProperty('overflow-y', 'auto', 'important');
            
            // Set transform based on state
            const isCollapsed = sidebar.getAttribute('aria-expanded') === 'false';
            if (!isCollapsed) {
                sidebar.style.setProperty('transform', 'translateX(0)', 'important');
                sidebar.style.setProperty('-webkit-transform', 'translateX(0)', 'important');
                if (!sidebar.getAttribute('aria-expanded') || sidebar.getAttribute('aria-expanded') === '') {
                    sidebar.setAttribute('aria-expanded', 'true');
                }
            } else {
                sidebar.style.setProperty('transform', 'translateX(-100%)', 'important');
                sidebar.style.setProperty('-webkit-transform', 'translateX(-100%)', 'important');
            }
        } else {
            console.log('Sidebar element not found in DOM!');
        }
    }
    
    function createToggle() {
        const existing = document.getElementById('custom-sidebar-toggle-btn');
        if (existing) return;
        
        const btn = document.createElement('button');
        btn.id = 'custom-sidebar-toggle-btn';
        btn.innerHTML = '☰';
        btn.setAttribute('aria-label', 'Toggle sidebar');
        btn.setAttribute('type', 'button');
        btn.style.cssText = 'position:fixed!important;top:1rem!important;left:1rem!important;z-index:999999!important;width:50px!important;height:50px!important;background:rgba(0,245,255,0.9)!important;border:3px solid #00f5ff!important;border-radius:8px!important;color:#fff!important;font-size:28px!important;cursor:pointer!important;box-shadow:0 4px 20px rgba(0,245,255,0.6)!important;display:flex!important;align-items:center!important;justify-content:center!important;pointer-events:auto!important;';
        
        btn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Try native toggle first
            const nativeToggle = document.querySelector('[data-testid="collapsedControl"]');
            if (nativeToggle) {
                nativeToggle.click();
                return;
            }
            
            // Manual toggle - Safari compatible
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                const isExpanded = sidebar.getAttribute('aria-expanded') !== 'false';
                if (isExpanded) {
                    sidebar.style.transform = 'translateX(-100%)';
                    sidebar.style.webkitTransform = 'translateX(-100%)';
                    sidebar.setAttribute('aria-expanded', 'false');
                } else {
                    sidebar.style.transform = 'translateX(0)';
                    sidebar.style.webkitTransform = 'translateX(0)';
                    sidebar.style.visibility = 'visible';
                    sidebar.style.display = 'block';
                    sidebar.setAttribute('aria-expanded', 'true');
                }
            }
        };
        
        if (document.body) {
            document.body.appendChild(btn);
            console.log('Toggle button created and added');
        }
    }
    
    function init() {
        console.log('Initializing sidebar...');
        ensureSidebarVisible();
        createToggle();
        
        // Double check after a brief delay
        setTimeout(function() {
            ensureSidebarVisible();
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                console.log('Sidebar found and made visible');
            } else {
                console.log('WARNING: Sidebar still not found!');
            }
        }, 100);
    }
    
    // Run immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Run multiple times to catch Streamlit's dynamic rendering
    setTimeout(init, 100);
    setTimeout(init, 500);
    setTimeout(init, 1000);
    setTimeout(init, 2000);
    setTimeout(init, 3000);
    setTimeout(init, 5000);
    
    // Watch for changes - very aggressive
    const obs = new MutationObserver(function(mutations) {
        ensureSidebarVisible();
        const toggleBtn = document.getElementById('custom-sidebar-toggle-btn');
        if (!toggleBtn) {
            createToggle();
        } else {
            toggleBtn.style.display = 'flex';
            toggleBtn.style.visibility = 'visible';
            toggleBtn.style.zIndex = '999999';
        }
    });
    
    if (document.body) {
        obs.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'aria-expanded']});
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            obs.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'aria-expanded']});
        });
    }
    
    window.addEventListener('load', init);
    
    // Check periodically
    setInterval(function() {
        ensureSidebarVisible();
        if (!document.getElementById('custom-sidebar-toggle-btn')) {
            createToggle();
        }
    }, 2000);
    </script>
    """, height=0)
    
    
    # Header - absolutely no top spacing - use negative margin to pull up
    st.markdown("""
    <div style="margin-top: -3rem !important; padding-top: 0 !important; margin-bottom: 0.25rem !important;">
        <h1 class="main-header" style="margin-top: 0 !important; padding-top: 0 !important; margin-bottom: 0 !important;">My Financial Dashboard</h1>
        <p class="subtitle" style="margin-top: 0 !important; padding-top: 0 !important; margin-bottom: 0 !important;">Track Your Spending, Income, and Savings Over Time - Demonstrated with dummy data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown("### 📊 FILTERS")
    
    # Reset filters button at the top of filters
    col_reset1, col_reset2 = st.sidebar.columns(2)
    with col_reset1:
        if st.sidebar.button("🔄 Reset", key="reset_filters", use_container_width=True):
            # Clear all filter keys from session state to reset to defaults
            for key in ['start_date', 'end_date', 'year_filter', 'product_filter', 'type_filter', 'category_filter',
                       'start_date_main', 'end_date_main', 'year_filter_main', 'category_filter_main']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col_reset2:
        if st.sidebar.button("🗑️ Clear Cache", key="clear_cache", use_container_width=True):
            # Clear the data cache
            load_data.clear()
            st.rerun()
    
    # Date Range - Improved handling
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    st.sidebar.markdown("**Date Range**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.get('start_date', min_date),
            min_value=min_date,
            max_value=max_date,
            key="start_date",
            label_visibility="collapsed"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=st.session_state.get('end_date', max_date),
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
    
    # Additional KPIs
    total_transactions = len(filtered_df) if len(filtered_df) > 0 else 0
    avg_transaction_size = abs(filtered_df['Amount'].mean()) if len(filtered_df) > 0 else 0
    avg_daily_spending = total_expenses / max(date_range_days, 1) if date_range_days > 0 else 0
    largest_expense = abs(filtered_df[filtered_df['Amount'] < 0]['Amount'].min()) if len(expenses_df) > 0 else 0
    largest_income = filtered_df[filtered_df['Amount'] > 0]['Amount'].max() if len(income_df) > 0 else 0
    unique_days = filtered_df['Date'].nunique() if len(filtered_df) > 0 else 0
    transactions_per_day = total_transactions / max(unique_days, 1) if unique_days > 0 else 0
    
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
    st.markdown("## My Financial Overview")
    
    # Calculate date range description for context
    if len(filtered_df) > 0:
        date_range_str = f"{filtered_df['Date'].min().strftime('%b %Y')} to {filtered_df['Date'].max().strftime('%b %Y')}"
        period_months = date_range_months
        if period_months < 1:
            period_description = f"({date_range_days} days)"
        elif period_months < 2:
            period_description = f"(~{int(period_months * 30)} days)"
        else:
            period_description = f"(~{period_months:.1f} months)"
    else:
        date_range_str = "No data"
        period_description = ""
    
    # Main metrics row - 4 columns (no background grouping)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #00f5ff;">
            <div class="metric-label">My Current Balance</div>
            <div class="metric-value">€{current_balance:,.2f}</div>
            <div style="font-size: 0.7rem; color: #a0a0a0; margin-top: 0.25rem; line-height: 1.3;">As of latest transaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #00f5ff;">
            <div class="metric-label">My Monthly Income</div>
            <div class="metric-value">€{avg_monthly_income:,.2f}</div>
            <div style="font-size: 0.7rem; color: #a0a0a0; margin-top: 0.25rem; line-height: 1.3;">Fixed monthly stipend</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ff00ff;">
            <div class="metric-label">My Average Monthly Expenses</div>
            <div class="metric-value">€{avg_monthly_expenses:,.2f}</div>
            <div style="font-size: 0.7rem; color: #a0a0a0; margin-top: 0.25rem; line-height: 1.3;">Average over selected period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        net_color = "#00f5ff" if net_flow >= 0 else "#ff00ff"
        net_label = "Total Saved" if net_flow >= 0 else "Total Spent Over Income"
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {net_color};">
            <div class="metric-label">{net_label}</div>
            <div class="metric-value">€{abs(net_flow):,.2f}</div>
            <div style="font-size: 0.7rem; color: #a0a0a0; margin-top: 0.25rem; line-height: 1.3;">Income - Expenses {period_description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional KPIs Row - 2 columns (no background grouping)
    col_kpi1, col_kpi2 = st.columns(2)
    
    with col_kpi1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ff00ff;">
            <div class="metric-label">Avg Daily Spending</div>
            <div class="metric-value" style="font-size: 1.6rem;">€{avg_daily_spending:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_kpi2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #00f5ff;">
            <div class="metric-label">Largest Expense</div>
            <div class="metric-value" style="font-size: 1.6rem;">€{largest_expense:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget Progress and Savings Rate - Cleaner style matching image
    st.markdown("### My Monthly Budget & Savings Rate")
    budget_col1, budget_col2 = st.columns([3, 1])  # Budget column much wider
    
    with budget_col1:
        # Budget card - cleaner style, blue when not exceeded, red when exceeded
        is_over_budget = current_month_expenses > monthly_budget
        budget_color = "#00f5ff" if not is_over_budget else "#ff0000"  # Blue when not exceeded, red when exceeded
        spent_color = "#00f5ff" if not is_over_budget else "#ff0000"
        
        st.markdown(f"""
        <div style="background: rgba(138, 43, 226, 0.08); backdrop-filter: blur(10px); padding: 1rem 1.25rem; border-radius: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: #a0a0a0; font-size: 0.75rem;">Spent this month</span>
                <span style="font-weight: 700; color: {spent_color}; font-size: 0.85rem;">€{current_month_expenses:,.2f} / <span style="color: #a0a0a0; font-weight: 400;">€{monthly_budget:,.2f}</span></span>
            </div>
            <div style="height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden; margin-bottom: 0.5rem;">
                <div style="height: 100%; width: {min(budget_used_pct, 100)}%; background: {budget_color}; transition: width 0.3s;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #a0a0a0; font-size: 0.7rem;">
                    {budget_used_pct:.1f}% used • €{max(budget_remaining, 0):,.2f} remaining
                </span>
                {'<span style="color: #ff0000; font-size: 0.7rem; font-weight: 700;">⚠️ BUDGET EXCEEDED!</span>' if is_over_budget else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with budget_col2:
        # Savings Rate - cleaner design matching budget style
        savings_color = "#00f5ff" if savings_rate >= 20 else "#ffd700" if savings_rate >= 0 else "#ff0000"
        # Determine period label for savings rate
        if period_months < 1:
            savings_period = f"{date_range_days} days"
        elif period_months < 2:
            savings_period = f"~{int(period_months * 30)} days"
        elif period_months < 12:
            savings_period = f"~{period_months:.1f} months"
        else:
            savings_period = f"~{period_months/12:.1f} years"
        
        st.markdown(f"""
        <div style="background: rgba(138, 43, 226, 0.08); backdrop-filter: blur(10px); padding: 1rem 1.25rem; border-radius: 12px;">
            <div style="color: #a0a0a0; font-size: 0.75rem; margin-bottom: 0.5rem;">Savings Rate</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 2.2rem; font-weight: 700; color: {savings_color}; line-height: 1;">{savings_rate:.1f}%</div>
                <div style="text-align: right;">
                    <div style="color: #a0a0a0; font-size: 0.7rem; margin-bottom: 0.25rem;">{savings_period}</div>
                    <div style="color: {savings_color}; font-size: 0.7rem; font-weight: 600;">{"Excellent" if savings_rate >= 20 else "Good" if savings_rate >= 0 else "Needs improvement"}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculate monthly summary (needed for waterfall chart)
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
    
    # Color palette - vibrant neon colors (needed for charts)
    colors = {
        'primary': '#00f5ff',
        'secondary': '#ff00ff',
        'accent': '#ffd700',
        'income': '#00f5ff',
        'expense': '#ff00ff',
        'positive': '#00f5ff',
        'negative': '#ff00ff'
    }
    
    # Reduced spacing divider
    st.markdown("<div style='margin: 0.25rem 0;'></div>", unsafe_allow_html=True)
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dashboard", 
        "Spending Analysis", 
        "Locations", 
        "Transactions",
        "Your AI Financial Advisor",
        "Methodology"
    ])
    
    # Weekday mapping for visualizations
    weekday_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 
                   'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    
    # Vibrant color palette for charts
    vibrant_colors = px.colors.qualitative.Vivid + px.colors.qualitative.Set3
    
    with tab1:
        # Dashboard header - first thing in Dashboard tab
        st.markdown("## My Financial Dashboard")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>View your account balance over time and see where your money goes.</p>", unsafe_allow_html=True)
        
        # Financial Health Score and Waterfall
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### My Financial Health Score")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>A visual indicator of your financial health based on your savings rate and spending patterns.</p>", unsafe_allow_html=True)
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
                st.plotly_chart(fig_gauge, use_container_width=True, key="gauge_chart_dashboard")
            
        with col2:
            st.markdown("### Monthly Income vs Expenses Waterfall")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>This chart shows how your monthly income and expenses add up over time. Each month's net amount (income minus expenses) is displayed.</p>", unsafe_allow_html=True)
            if len(monthly_summary) > 0:
                waterfall_data = monthly_summary.copy()
                waterfall_data['Net_Flow'] = waterfall_data['Net']
                
                fig_waterfall = go.Figure(go.Waterfall(
                    name="Income Minus Expenses",
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
                    yaxis_title="Amount (€) - Income Minus Expenses",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    showlegend=False,
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_waterfall, use_container_width=True, key="waterfall_chart_dashboard")
        
        # Balance Over Time and Top Categories - Side by Side
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### My Account Balance Over Time")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Track how your account balance changes with each transaction. The dashed line shows your current balance.</p>", unsafe_allow_html=True)
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
                    height=300,
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
            st.markdown("### My Top Spending Categories")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>See which categories account for most of your expenses.</p>", unsafe_allow_html=True)
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
                    height=300,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=False, categoryorder='total ascending')
                )
                st.plotly_chart(fig_categories, use_container_width=True, key="top_categories_bar")
            else:
                st.info("No expense data available.")
        
        # Income vs Expenses Chart
        st.markdown("### My Monthly Income vs Expenses")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Compare your monthly income and expenses side by side. The line shows your net amount (income minus expenses) each month.</p>", unsafe_allow_html=True)
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
                name='Income Minus Expenses',
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
        st.markdown("### My Expenses by Category")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>A detailed breakdown of all your spending categories. Hover over bars to see exact amounts.</p>", unsafe_allow_html=True)
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
        
        # Advanced Transaction Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Transaction Size vs Balance")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>See how individual transaction amounts relate to your account balance at that time.</p>", unsafe_allow_html=True)
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
                        height=300,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_balance")
        
        with col2:
            st.markdown("#### 3D Scatter: Amount vs Hour vs Day")
            st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Explore spending patterns across different times of day and days of the week.</p>", unsafe_allow_html=True)
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
                        height=300,
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
        
    with tab2:
        st.markdown("## My Spending Analysis")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 0.5rem; margin-top: 0.1rem;'>Analyze your spending patterns by category, time, and location to understand where your money goes.</p>", unsafe_allow_html=True)
        
        if len(expenses_df) > 0:
            # Key Insights - At the top for quick summary
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
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
                avg_expense = expenses_df['Amount_Abs'].mean()
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 0.875rem; color: #a0a0a0; margin-bottom: 0.5rem;">Average Transaction</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">€{avg_expense:,.2f}</div>
                    <div style="font-size: 1rem; color: {colors['primary']}; margin-top: 0.5rem;">per transaction</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Category Analysis Section
            st.markdown("### Category Analysis")
            st.markdown("<p style='font-size: 0.75rem; color: #a0a0a0; margin-bottom: 0.5rem; margin-top: 0.1rem;'>Understand how your spending is distributed across different categories and how it evolves over time.</p>", unsafe_allow_html=True)
            
            st.markdown("#### Spending by Category")
            st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Compare spending amounts across different categories. Hover to see exact values.</p>", unsafe_allow_html=True)
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
            
            # Category Trends Section
            col_cat1, col_cat2 = st.columns(2)
            
            with col_cat1:
                st.markdown("#### Category Trends Over Time")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Track how your top spending categories change month by month.</p>", unsafe_allow_html=True)
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
                        height=300,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_trends, use_container_width=True, key="category_trends")
                else:
                    st.info("No trend data available.")
            
            with col_cat2:
                st.markdown("#### Average Spending per Transaction by Category")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>See which categories typically have higher transaction amounts.</p>", unsafe_allow_html=True)
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
                        height=300,
                        margin=dict(l=0, r=0, t=0, b=0),
                        showlegend=False,
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_avg_cat, use_container_width=True, key="avg_category_spending")
            
            # Stacked Area Chart
            st.markdown("#### Stacked Area: Category Trends")
            st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Visualize cumulative spending by category over time.</p>", unsafe_allow_html=True)
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
                        height=300,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        legend=dict(font=dict(color='#ffffff', size=11))
                    )
                    st.plotly_chart(fig_area, use_container_width=True, key="stacked_area")
            
            # Temporal Patterns Section
            st.markdown("### Temporal Patterns")
            st.markdown("<p style='font-size: 0.75rem; color: #a0a0a0; margin-bottom: 0.5rem; margin-top: 0.1rem;'>Explore when during the day and week you tend to spend the most.</p>", unsafe_allow_html=True)
            
            col_temp1, col_temp2 = st.columns(2)
            
            with col_temp1:
                st.markdown("#### Spending by Day of Week")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Discover which days of the week you spend the most.</p>", unsafe_allow_html=True)
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
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_weekday, use_container_width=True, key="weekday_spending")
            
            with col_temp2:
                st.markdown("#### Spending by Hour of Day")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Track your spending patterns throughout the day to identify peak spending hours.</p>", unsafe_allow_html=True)
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
            
            # Spending Heatmap
            st.markdown("#### Spending Heatmap: Day vs Hour")
            st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.1rem; margin-top: 0.1rem;'>Visualize spending intensity across days and hours. Darker colors indicate higher spending.</p>", unsafe_allow_html=True)
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
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig_heatmap, use_container_width=True, key="spending_heatmap_trends_tab")
            
            # Top Merchants
            st.markdown("### Top Merchants")
            st.markdown("<p style='font-size: 0.75rem; color: #a0a0a0; margin-bottom: 0.5rem; margin-top: 0.1rem;'>See which merchants and locations account for most of your spending.</p>", unsafe_allow_html=True)
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
    
    with tab3:
        st.markdown("## Location-Based Spending Analysis")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 1rem;'>Explore your spending patterns across different countries and cities with interactive visualizations.</p>", unsafe_allow_html=True)
        
        if 'Country' in filtered_df.columns and filtered_df['Country'].nunique() > 1:
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_metrics = expenses_df.groupby('Country').agg({
                    'Amount_Abs': ['sum', 'mean', 'count']
                }).reset_index()
                country_metrics.columns = ['Country', 'Total_Spending', 'Avg_Transaction', 'Transaction_Count']
                country_metrics = country_metrics.sort_values('Total_Spending', ascending=False)
                
                # Interactive Country Selector
                st.markdown("### Interactive Country Explorer")
                selected_countries = st.multiselect(
                    "Select countries to analyze (leave empty for all)",
                    options=country_metrics['Country'].tolist(),
                    default=[],
                    key="country_selector"
                )
                
                if selected_countries:
                    filtered_expenses = expenses_df[expenses_df['Country'].isin(selected_countries)]
                    country_metrics_filtered = country_metrics[country_metrics['Country'].isin(selected_countries)]
                else:
                    filtered_expenses = expenses_df
                    country_metrics_filtered = country_metrics
                
                # Key Metrics
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    total_countries = len(country_metrics_filtered)
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #00f5ff;">
                        <div class="metric-label">Countries</div>
                        <div class="metric-value">{total_countries}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    top_country = country_metrics_filtered.iloc[0]['Country'] if len(country_metrics_filtered) > 0 else 'N/A'
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #00f5ff;">
                        <div class="metric-label">Top Country</div>
                        <div class="metric-value" style="font-size: 1.5rem;">{top_country}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    top_spending = country_metrics_filtered.iloc[0]['Total_Spending'] if len(country_metrics_filtered) > 0 else 0
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                        <div class="metric-label">Highest Spending</div>
                        <div class="metric-value">€{top_spending:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col4:
                    total_spending_filtered = filtered_expenses['Amount_Abs'].sum() if len(filtered_expenses) > 0 else 0
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid #ff00ff;">
                        <div class="metric-label">Total Selected</div>
                        <div class="metric-value">€{total_spending_filtered:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # World Map Visualization - Keep the cool map!
            st.markdown("### 🌍 Interactive World Map")
            st.markdown("<p style='font-size: 0.75rem; color: #a0a0a0; margin-bottom: 0.5rem;'>Click on countries to see detailed spending information. Hover for more details.</p>", unsafe_allow_html=True)
            if len(filtered_expenses) > 0 and 'Country' in filtered_expenses.columns:
                country_spending_map = filtered_expenses.groupby('Country')['Amount_Abs'].sum().reset_index()
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
                        height=350,
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
            
            # Cool Visualizations Section
            # Cool Visualizations Section

            # =======================
            # Row 1: Bubble + Sunburst
            # =======================
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Bubble Chart: Country Comparison")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>Bubble size = transaction count, Color = total spending</p>", unsafe_allow_html=True)
                if len(country_metrics_filtered) > 0:
                    fig_bubble = px.scatter(
                        country_metrics_filtered,
                        x='Avg_Transaction',
                        y='Total_Spending',
                        size='Transaction_Count',
                        color='Total_Spending',
                        hover_name='Country',
                        hover_data=['Avg_Transaction', 'Transaction_Count'],
                        color_continuous_scale='Plasma',
                        title="",
                        labels={'Avg_Transaction': 'Avg Transaction (€)', 'Total_Spending': 'Total Spending (€)'}
                    )
                    fig_bubble.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig_bubble, use_container_width=True, key="country_bubble")


            with col2:
                if 'City' in filtered_expenses.columns and filtered_expenses['City'].nunique() > 1:
                    st.markdown("#### Sunburst: Country → City → Category Hierarchy")
                    st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>Interactive hierarchy: Click segments to explore deeper levels.</p>", unsafe_allow_html=True)
                    if len(filtered_expenses) > 0:
                        hierarchy_data = filtered_expenses.groupby(['Country', 'City', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                        hierarchy_data = hierarchy_data.sort_values('Amount_Abs', ascending=False).head(100)

                        fig_sunburst = px.sunburst(
                            hierarchy_data,
                            path=['Country', 'City', 'Merchant_Category'],
                            values='Amount_Abs',
                            color='Amount_Abs',
                            color_continuous_scale='Plasma',
                            title=""
                        )
                        fig_sunburst.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#ffffff',
                            height=400,
                            margin=dict(l=0, r=0, t=0, b=0)
                        )
                        st.plotly_chart(fig_sunburst, use_container_width=True, key="sunburst_hierarchy")


            # =======================
            # Row 2: Trends + Heatmap
            # =======================
            st.markdown("### 📈 Country Comparison & Trends")

            col_trend1, col_trend2 = st.columns(2)

            with col_trend1:
                st.markdown("#### Monthly Trends by Country")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>Track spending evolution over time. Click legend to toggle countries.</p>", unsafe_allow_html=True)

                if len(filtered_expenses) > 0 and 'Date' in filtered_expenses.columns:
                    expenses_trend = filtered_expenses.copy()
                    expenses_trend['YearMonth'] = expenses_trend['Date'].dt.to_period('M').astype(str)
                    country_monthly = expenses_trend.groupby(['YearMonth', 'Country'])['Amount_Abs'].sum().reset_index()

                    if len(country_monthly) > 0:
                        fig_trend = px.line(
                            country_monthly,
                            x='YearMonth',
                            y='Amount_Abs',
                            color='Country',
                            markers=True,
                            color_discrete_sequence=vibrant_colors
                        )
                        fig_trend.update_traces(line=dict(width=3), marker=dict(size=8))
                        fig_trend.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#ffffff',
                            hovermode='x unified',
                            height=400,
                            margin=dict(l=0, r=0, t=0, b=0),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickangle=-45),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                            legend=dict(font=dict(color='#ffffff', size=11), bgcolor='rgba(0,0,0,0.5)')
                        )
                        st.plotly_chart(fig_trend, use_container_width=True, key="country_trends")


            with col_trend2:
                st.markdown("#### Category Heatmap by Country")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>See which categories dominate in each country.</p>", unsafe_allow_html=True)

                if len(filtered_expenses) > 0:
                    heatmap_data = filtered_expenses.groupby(['Country', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                    if len(heatmap_data) > 0:
                        heatmap_pivot = heatmap_data.pivot(index='Merchant_Category', columns='Country', values='Amount_Abs').fillna(0)

                        fig_heatmap = px.imshow(
                            heatmap_pivot,
                            labels=dict(x="Country", y="Category", color="Spending (€)"),
                            color_continuous_scale='Plasma',
                            aspect="auto",
                            text_auto=True
                        )
                        fig_heatmap.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#ffffff',
                            height=400,
                            margin=dict(l=0, r=0, t=0, b=0)
                        )
                        st.plotly_chart(fig_heatmap, use_container_width=True, key="heatmap_country_category")


            # =======================
            # Row 3: City Bar + Area
            # =======================
            col_city, col_area = st.columns(2)

            with col_city:
                st.markdown("#### City Spending Comparison")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>Horizontal bar chart for easy comparison.</p>", unsafe_allow_html=True)

                city_spending_bar = filtered_expenses.groupby('City')['Amount_Abs'].sum().reset_index()
                city_spending_bar = city_spending_bar.sort_values('Amount_Abs', ascending=True).tail(10)

                if len(city_spending_bar) > 0:
                    fig_city_bar = px.bar(
                        city_spending_bar,
                        x='Amount_Abs',
                        y='City',
                        orientation='h',
                        color='Amount_Abs',
                        color_continuous_scale='Plasma',
                        text='Amount_Abs'
                    )
                    fig_city_bar.update_traces(
                        texttemplate='€%{text:,.0f}',
                        textposition='outside',
                        textfont=dict(color='#ffffff', size=10)
                    )
                    fig_city_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#ffffff',
                        height=400,
                        margin=dict(l=0, r=0, t=30, b=0),
                        showlegend=False
                    )
                    st.plotly_chart(fig_city_bar, use_container_width=True)


            with col_area:
                st.markdown("#### Stacked Area: Cumulative Spending by Country")
                st.markdown("<p style='font-size: 0.7rem; color: #a0a0a0; margin-bottom: 0.5rem;'>See how spending accumulates over time across countries.</p>", unsafe_allow_html=True)

                if len(filtered_expenses) > 0 and 'Date' in filtered_expenses.columns:
                    expenses_area = filtered_expenses.copy()
                    expenses_area['YearMonth'] = expenses_area['Date'].dt.to_period('M').astype(str)
                    country_area = expenses_area.groupby(['YearMonth', 'Country'])['Amount_Abs'].sum().reset_index()

                    if len(country_area) > 0:
                        fig_area = px.area(
                            country_area,
                            x='YearMonth',
                            y='Amount_Abs',
                            color='Country',
                            color_discrete_sequence=vibrant_colors
                        )
                        fig_area.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#ffffff',
                            height=400,
                            margin=dict(l=0, r=0, t=30, b=0),
                            xaxis=dict(tickangle=-45)
                        )
                        st.plotly_chart(fig_area, use_container_width=True)

            
            
           
                
    
    with tab4:
        st.markdown("## Transaction Details")
        
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] label {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
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
            st.markdown("""
            <style>
            div[data-testid="stDownloadButton"] button {
                color: black !important;
            }
            div[data-testid="stDownloadButton"] button p {
                color: black !important;
            }
            div[data-testid="stDownloadButton"] button span {
                color: black !important;
            }
            div[data-testid="stDownloadButton"] > button {
                color: black !important;
            }
            button[kind="secondary"] {
                color: black !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.download_button(
                label="Download Filtered Data",
                data=csv,
                file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No transactions found matching your search criteria.")
    
    with tab5:
        # Add CSS for white bubbles at the start
        st.markdown("""
        <style>
        .assistant-bubble {
            background-color: #ffffff !important;
            color: #000000 !important;
            padding: 1rem 1.5rem !important;
            border-radius: 20px !important;
            margin: 0.5rem 0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
            display: inline-block !important;
            max-width: 90% !important;
        }
        /* Ensure markdown container doesn't override */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"][aria-label="assistant"]) div[data-testid="stMarkdownContainer"] {
            background-color: transparent !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🤖 Your AI Financial Advisor")
        st.markdown("<p style='font-size: 0.8rem; color: #a0a0a0; margin-bottom: 1rem;'>Ask me anything about your financial data! I can help you understand your spending patterns, identify trends, and provide insights.</p>", unsafe_allow_html=True)
        
        # API Key setup for Gemini
        use_ai = False
        if GEMINI_AVAILABLE:
            # Check for API key in environment or session state
            api_key = os.getenv("GEMINI_API_KEY") or st.session_state.get("gemini_api_key", "")
            
            if not api_key:
                with st.expander("🔑 Enable AI (Free - Google Gemini)", expanded=False):
                    st.markdown("""
                    **Get your free API key:**
                    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
                    2. Sign in with your Google account
                    3. Click "Create API Key"
                    4. Paste it below
                    
                    The free tier includes generous usage limits!
                    """)
                    api_key_input = st.text_input("Enter your Gemini API Key:", type="password", key="api_key_input")
                    if api_key_input:
                        st.session_state.gemini_api_key = api_key_input
                        api_key = api_key_input
                        st.success("✅ API key saved! Refresh to use AI.")
            
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    use_ai = True
                except Exception as e:
                    st.warning(f"⚠️ Error configuring Gemini: {e}. Using rule-based responses.")
        
        # Initialize chat history
        if "advisor_messages" not in st.session_state:
            st.session_state.advisor_messages = []
        
        # Display chat history
        for message in st.session_state.advisor_messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    # Use st.markdown with HTML for white bubble background
                    import html
                    import re
                    content = message["content"]
                    # Escape HTML first
                    escaped_content = html.escape(content)
                    # Convert markdown bold (**text**) to HTML bold
                    def replace_bold(match):
                        return f'<strong style="font-weight: bold;">{match.group(1)}</strong>'
                    formatted_content = re.sub(r'\*\*(.+?)\*\*', replace_bold, escaped_content)
                    # Replace newlines with <br>
                    formatted_content = formatted_content.replace('\n', '<br>')
                    # White bubble background with rounded corners - use class for CSS targeting
                    bubble_html = f'<div class="assistant-bubble" style="background-color: #ffffff; color: #000000; padding: 1rem 1.5rem; border-radius: 20px; margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); display: inline-block; max-width: 90%;">{formatted_content}</div>'
                    st.markdown(bubble_html, unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])
        
        # Function to prepare financial data context
        def prepare_financial_context(expenses_df, income_df, monthly_summary):
            """Prepare a comprehensive financial data summary for AI context"""
            total_expenses = expenses_df['Amount_Abs'].sum() if len(expenses_df) > 0 else 0
            total_income = income_df['Amount'].sum() if len(income_df) > 0 else 0
            net_flow = total_income - total_expenses
            savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
            
            context = f"""Financial Data Summary:
- Total Expenses: €{total_expenses:,.2f} ({len(expenses_df)} transactions)
- Total Income: €{total_income:,.2f} ({len(income_df)} transactions)
- Net Flow: €{net_flow:,.2f}
- Savings Rate: {savings_rate:.1f}%

"""
            
            # Top spending categories
            if len(expenses_df) > 0:
                category_spending = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().sort_values(ascending=False)
                context += "Top Spending Categories:\n"
                for i, (cat, amt) in enumerate(category_spending.head(10).items(), 1):
                    context += f"{i}. {cat}: €{amt:,.2f}\n"
                context += "\n"
            
            # Monthly summary
            if len(monthly_summary) > 0:
                context += "Monthly Breakdown:\n"
                for _, row in monthly_summary.iterrows():
                    context += f"- {row['Month']}: Income €{row['Income']:,.2f}, Expenses €{row['Expenses']:,.2f}, Net €{row['Net']:,.2f}\n"
                context += "\n"
            
            return context
        
        # Function to analyze data and generate response (AI-powered or rule-based)
        def analyze_financial_question(question, filtered_df, expenses_df, income_df, monthly_summary):
            # Try AI first if available
            if use_ai and GEMINI_AVAILABLE:
                try:
                    # Prepare financial context
                    context = prepare_financial_context(expenses_df, income_df, monthly_summary)
                    
                    # Create prompt for Gemini
                    prompt = f"""You are a helpful financial advisor analyzing a user's financial data. 
Answer their question based on the following financial data summary. Be concise, friendly, and use markdown formatting for numbers and emphasis.

Financial Data:
{context}

User Question: {question}

Provide a clear, helpful answer based on the data above. Use **bold** for important numbers and insights."""
                    
                    # Generate response using Gemini
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    return response.text
                    
                except Exception as e:
                    # Fall back to rule-based if AI fails
                    st.warning(f"AI error: {e}. Using rule-based response.")
            
            # Rule-based fallback (original logic)
            question_lower = question.lower()
            
            # Calculate key metrics
            total_expenses = expenses_df['Amount_Abs'].sum() if len(expenses_df) > 0 else 0
            total_income = income_df['Amount'].sum() if len(income_df) > 0 else 0
            avg_expense = expenses_df['Amount_Abs'].mean() if len(expenses_df) > 0 else 0
            largest_expense = expenses_df['Amount_Abs'].max() if len(expenses_df) > 0 else 0
            
            # Category analysis
            if len(expenses_df) > 0:
                category_spending = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().sort_values(ascending=False)
                top_category = category_spending.index[0] if len(category_spending) > 0 else "N/A"
                top_category_amount = category_spending.iloc[0] if len(category_spending) > 0 else 0
            else:
                top_category = "N/A"
                top_category_amount = 0
            
            # Monthly analysis
            if len(monthly_summary) > 0:
                best_month = monthly_summary.loc[monthly_summary['Net'].idxmax(), 'Month'] if len(monthly_summary) > 0 else "N/A"
                worst_month = monthly_summary.loc[monthly_summary['Net'].idxmin(), 'Month'] if len(monthly_summary) > 0 else "N/A"
            else:
                best_month = "N/A"
                worst_month = "N/A"
            
            # Answer generation based on question keywords
            if any(word in question_lower for word in ["spend", "expense", "cost", "money"]):
                if "category" in question_lower or "where" in question_lower:
                    response = f"Based on your data, you've spent **€{total_expenses:,.2f}** in the selected period. "
                    if top_category != "N/A":
                        response += f"Your top spending category is **{top_category}** with **€{top_category_amount:,.2f}**. "
                    if len(category_spending) > 1:
                        response += f"Here are your top 5 categories:\n"
                        for i, (cat, amt) in enumerate(category_spending.head(5).items(), 1):
                            response += f"{i}. {cat}: €{amt:,.2f}\n"
                elif "average" in question_lower or "avg" in question_lower:
                    response = f"Your average transaction amount is **€{avg_expense:,.2f}**. "
                    response += f"You have **{len(expenses_df)}** expense transactions in the selected period."
                elif "largest" in question_lower or "biggest" in question_lower or "most" in question_lower:
                    response = f"Your largest single expense is **€{largest_expense:,.2f}**. "
                    if len(expenses_df) > 0:
                        largest_row = expenses_df.loc[expenses_df['Amount_Abs'].idxmax()]
                        response += f"This was in the **{largest_row.get('Merchant_Category', 'Unknown')}** category."
                else:
                    response = f"You've spent a total of **€{total_expenses:,.2f}** in the selected period. "
                    response += f"This is based on **{len(expenses_df)}** expense transactions."
            
            elif any(word in question_lower for word in ["income", "earn", "revenue"]):
                response = f"Your total income in the selected period is **€{total_income:,.2f}**. "
                response += f"This comes from **{len(income_df)}** income transactions."
            
            elif any(word in question_lower for word in ["save", "saving", "net", "balance"]):
                net_flow = total_income - total_expenses
                savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
                response = f"Your net flow (income minus expenses) is **€{net_flow:,.2f}**. "
                response += f"Your savings rate is **{savings_rate:.1f}%**. "
                if net_flow > 0:
                    response += "Great job! You're saving money. 💰"
                else:
                    response += "You're spending more than you earn. Consider reviewing your expenses. 💡"
            
            elif any(word in question_lower for word in ["month", "monthly", "best", "worst"]):
                if best_month != "N/A" and worst_month != "N/A":
                    best_net = monthly_summary.loc[monthly_summary['Month'] == best_month, 'Net'].iloc[0]
                    worst_net = monthly_summary.loc[monthly_summary['Month'] == worst_month, 'Net'].iloc[0]
                    response = f"Your best month was **{best_month}** with a net of **€{best_net:,.2f}**. "
                    response += f"Your worst month was **{worst_month}** with a net of **€{worst_net:,.2f}**. "
                else:
                    response = "I need more monthly data to compare months. Try adjusting your date range filter."
            
            elif any(word in question_lower for word in ["trend", "pattern", "over time", "change"]):
                if len(monthly_summary) > 0:
                    response = f"Looking at your monthly trends:\n"
                    for _, row in monthly_summary.tail(6).iterrows():
                        response += f"- **{row['Month']}**: Income €{row['Income']:,.2f}, Expenses €{row['Expenses']:,.2f}, Net €{row['Net']:,.2f}\n"
                else:
                    response = "I need more data to analyze trends. Try adjusting your date range filter."
            
            elif any(word in question_lower for word in ["help", "what can", "how", "advice", "recommend"]):
                response = """I can help you understand:
- **Spending patterns**: Ask about your expenses, categories, or where your money goes
- **Income analysis**: Questions about your earnings
- **Savings**: Net flow, savings rate, and financial health
- **Trends**: Monthly comparisons and patterns over time
- **Categories**: Top spending categories and breakdowns

Try asking questions like:
- "Where do I spend the most money?"
- "What's my average expense?"
- "What's my savings rate?"
- "Which month was my best?"
- "Show me my spending trends"
"""
            else:
                # Default response when question is not understood
                response = "I'm sorry, I may not have fully understood your question. Could you please rephrase it? I can help you with:\n\n"
                response += "- **Spending analysis**: Questions about expenses, categories, or where your money goes\n"
                response += "- **Income**: Questions about your earnings\n"
                response += "- **Savings**: Net flow, savings rate, and financial health\n"
                response += "- **Trends**: Monthly comparisons and patterns over time\n"
                response += "- **Categories**: Top spending categories and breakdowns\n\n"
                response += "Try asking something like: 'Where do I spend the most?' or 'What's my savings rate?'"
            
            return response
        
        # Chat input - must be after displaying chat history
        if prompt := st.chat_input("Ask me about your finances..."):
            # Add user message to chat history FIRST
            st.session_state.advisor_messages.append({"role": "user", "content": prompt})
            
            # Generate response
            response = analyze_financial_question(
                prompt, 
                filtered_df, 
                expenses_df, 
                income_df, 
                monthly_summary
            )
            
            # Add assistant response to chat history
            st.session_state.advisor_messages.append({"role": "assistant", "content": response})
            
            # Rerun to display the new messages
            st.rerun()
        
        # Quick question suggestions
        st.markdown("---")
        st.markdown("### 💡 Quick Questions")
        col_q1, col_q2, col_q3 = st.columns(3)
        
        with col_q1:
            if st.button("Where do I spend the most?", use_container_width=True, key="q1"):
                question = "Where do I spend the most money?"
                if question not in [msg["content"] for msg in st.session_state.advisor_messages if msg["role"] == "user"]:
                    st.session_state.advisor_messages.append({"role": "user", "content": question})
                    response = analyze_financial_question(question, filtered_df, expenses_df, income_df, monthly_summary)
                    st.session_state.advisor_messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        with col_q2:
            if st.button("What's my savings rate?", use_container_width=True, key="q2"):
                question = "What's my savings rate?"
                if question not in [msg["content"] for msg in st.session_state.advisor_messages if msg["role"] == "user"]:
                    st.session_state.advisor_messages.append({"role": "user", "content": question})
                    response = analyze_financial_question(question, filtered_df, expenses_df, income_df, monthly_summary)
                    st.session_state.advisor_messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        with col_q3:
            if st.button("Show spending trends", use_container_width=True, key="q3"):
                question = "Show me my spending trends"
                if question not in [msg["content"] for msg in st.session_state.advisor_messages if msg["role"] == "user"]:
                    st.session_state.advisor_messages.append({"role": "user", "content": question})
                    response = analyze_financial_question(question, filtered_df, expenses_df, income_df, monthly_summary)
                    st.session_state.advisor_messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.advisor_messages = []
            st.rerun()
        
        
        
        

        
        
    
    with tab6:
        st.markdown("## Methodology & Design")
        st.markdown("<p style='font-size: 0.9rem; color: #a0a0a0; margin-bottom: 1rem;'>This page explains the design choices, visual encodings, and methodology behind this dashboard, following Munzner's nested model for visualization design.</p>", unsafe_allow_html=True)
        
        # Overview
        st.markdown("""
        ### Project Overview
        
        This interactive financial analytics dashboard transforms transaction data into actionable insights, enabling users 
        to understand spending patterns, track financial health, and make informed decisions. Designed for individuals 
        managing personal finances, particularly useful for students and professionals tracking expenses across multiple 
        locations and time periods.
        
        **Target Audience**: Primary user is myself (Erasmus Mundus student), but applicable to anyone managing personal finances.
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
            - Category trends over time (line charts and stacked area)
            - Spending heatmaps (day vs hour patterns)
            - Key insights (top category, peak hours, averages)
            - Seasonal patterns
            """)
        
        # Data Structure
        st.markdown("### Data Structure")
        
        st.markdown("""
        **Data Types & Variables:**
        
        - **Temporal**: Date, Year, Month, Day, Weekday, Hour (enables time-series analysis)
        - **Financial**: Amount (signed), Balance (cumulative), Amount_Abs (absolute value for expenses)
        - **Categorical**: Type (transaction type), Product (account type), Merchant_Category (spending category)
        - **Geographic**: Country, City (enables location-based analysis)
        - **Descriptive**: Description_Anon (anonymized transaction descriptions)
        
        **Data Source**: Personal bank transaction exports (CSV format), anonymized for privacy. Dataset spans ~20 months 
        with transactions across 4 countries (Belgium, Spain, Germany, France) as part of Erasmus Mundus program.
        """)
        
        # Visual Representations
        st.markdown("### Visual Representations & Encodings")
        
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.markdown("""
            **Chart Types & Rationale:**
            
            - **Area Chart** (Balance): Shows cumulative effect over time, area encoding emphasizes trend magnitude
            - **Grouped Bar Chart** (Income vs Expenses): Direct comparison, position encoding for precise values
            - **Pie Chart** (Categories): Part-to-whole relationships, angle encoding for proportions
            - **Heatmap** (Day × Hour): 2D temporal patterns, color intensity encoding reveals patterns
            - **Line Chart** (Trends): Evolution over time, position encoding for trends
            - **Treemap** (Category Hierarchy): Hierarchical size comparison, area encoding for magnitude
            - **Sunburst** (Multi-level): Nested hierarchies, angle + radius encoding
            - **3D Scatter** (Multi-variate): Three quantitative variables, position encoding in 3D space
            - **Waterfall** (Net Flow): Cumulative changes, position encoding shows flow
            - **Gauge** (Health Score): Single metric with context, angle encoding with color zones
            """)
        
        with col_v2:
            st.markdown("""
            **Encoding Choices:**
            
            - **Position** (x/y axes): Most accurate for quantitative comparisons
            - **Color**: Used for categories (nominal) and amounts (quantitative via color scales)
            - **Size**: Area/bar height for magnitude comparisons
            - **Angle**: Pie charts for proportions
            - **Shape**: Not used (limited expressivity for this data)
            
            **Why These Encodings:**
            
            Following Cleveland & McGill's accuracy ranking: Position > Length > Angle > Area > Color > Volume.
            Critical comparisons use position (bars), less critical use color (heatmaps). Color also used for 
            categorical distinction (income=cyan, expenses=magenta) following financial conventions.
            """)
        
        # Page Layout & Screenspace
        st.markdown("### Page Layout & Screenspace Use")
        
        st.markdown("""
        **Layout Structure:**
        
        - **Wide Layout** (Streamlit): Maximizes horizontal space for time-series charts, optimal for temporal data
        - **Tabbed Interface**: Organizes 6 main sections (Dashboard, Spending Analysis, Locations, Transactions, Your AI Financial Advisor, Methodology), reduces cognitive load, allows focused exploration
        - **Sidebar Filters**: Always visible, persistent state, enables dynamic filtering without losing context
        - **Top Metrics Section**: Key numbers prominently displayed in card layout, glassmorphism design
        - **Column Layouts**: 2-4 column grids for comparison visualizations, responsive to screen size
        - **Consolidated Spending Tab**: Combines spending analysis with trends and insights for comprehensive view
        
        **Screenspace Optimization:**
        
        - Aggressive spacing reduction (margins, padding minimized) to fit more content
        - Compact chart heights (300-400px) while maintaining readability
        - Efficient use of vertical space with stacked sections
        - Removed Streamlit default headers/footers to maximize content area
        - Grouped related metrics in cards with shared backgrounds
        """)
        
        # Interaction
        st.markdown("### Interaction Design")
        
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.markdown("""
            **Filtering Interactions:**
            
            - **Date Range Picker**: Filter by specific time periods
            - **Year Selector**: Focus on specific years
            - **Category Multi-select**: Analyze specific spending categories
            - **Type Filter**: Separate income vs expenses
            - **Reset Button**: Clear all filters quickly
            - **Real-time Updates**: All visualizations update immediately on filter change
            
            **Impact**: Enables exploratory data analysis, answer ad-hoc questions, drill down into specific periods/categories.
            """)
        
        with col_i2:
            st.markdown("""
            **Chart Interactions:**
            
            - **Zoom/Pan**: Click and drag to zoom into time periods (Plotly default)
            - **Hover Tooltips**: See exact values, dates, amounts without cluttering
            - **Legend Toggle**: Click legend items to show/hide series
            - **Box Select**: Select ranges for detailed view
            - **Download**: Export charts as PNG
            - **Data Export**: Download filtered transaction data as CSV
            
            **Impact**: Detailed exploration without overwhelming interface, supports both overview and detail views.
            """)
        
        # Color Use
        st.markdown("### Color Use & Design Aesthetics")
        
        st.markdown("""
        **Color Palette:**
        
        - **Primary (Cyan #00f5ff)**: Income, positive values, primary actions (financial convention: "money in")
        - **Secondary (Magenta #ff00ff)**: Expenses, negative values, warnings (financial convention: "money out")
        - **Accent (Gold #ffd700)**: Important metrics, savings rate, warnings
        - **Background**: Dark theme (#0a0e27) reduces eye strain, modern aesthetic
        - **Purple Accents**: Grouping elements, decorative borders (rgba(138, 43, 226, 0.08))
        
        **Color Encoding Rationale:**
        
        - **Categorical**: Distinct colors for different categories (using Plotly's qualitative palettes)
        - **Quantitative**: Color intensity/scale for amounts (Plasma, Vivid scales)
        - **Semantic**: Cyan/Magenta follow financial conventions (green=income, red=expenses, adapted to theme)
        - **Accessibility**: High contrast ratios, colorblind-friendly palettes where possible
        
        **Design Aesthetics:**
        
        - **Glassmorphism**: Translucent cards with backdrop blur for modern look
        - **Gradient Borders**: Decorative elements for visual interest
        - **Consistent Spacing**: Reduced margins for information density
        - **Typography**: Clear hierarchy, readable fonts, appropriate sizes
        """)
        
        # Technology & Implementation
        st.markdown("### Technology Stack & Implementation")
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("""
            **Technology Choices:**
            
            - **Streamlit**: Web framework for rapid development
              - Trade-off: Ease of use vs expressivity
              - Chosen for: Fast development, Python integration, good balance
              - Alternative considered: D3.js (more expressive but slower)
            
            - **Plotly**: Interactive visualizations
              - Rich interactivity out-of-the-box
              - Publication-quality charts
              - Good performance with large datasets
            
            - **Pandas**: Data manipulation
              - Efficient aggregation and filtering
              - Time-series operations
            """)
        
        with col_t2:
            st.markdown("""
            **Implementation Features:**
            
            - **Data Caching**: `@st.cache_data` for performance, auto-invalidation on file change
            - **Error Handling**: Graceful degradation when data missing
            - **Responsive Design**: Adapts to different screen sizes
            - **Performance**: Optimized aggregations, efficient filtering
            - **Code Organization**: Modular structure, clear separation of concerns
            
            **Metadata:**
            
            - All visualizations include titles and descriptions
            - Tooltips show detailed information
            - Methodology page documents all choices
            - README provides setup instructions
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
            - Budget planning and adherence
            - Cost of living comparison across locations
            - Natural language queries via AI Financial Advisor
            """)
        
        with col_u2:
            st.markdown("""
        **Current Limitations**
        
        - Transaction-level data only (no investments/assets tracking)
        - Manual CSV import (no real-time API integration)
        - Single monthly budget (no category-specific budgets)
        - No forecasting capabilities or predictive analytics
        - Location data may be incomplete for some transactions
        - No multi-currency support (assumes single currency)
        - Limited to historical data (no real-time updates)
        - Trends analysis consolidated into Spending Analysis tab (no separate trends tab)
        - AI Financial Advisor uses rule-based system (optional AI integration available)
            """)
        
        # AI Financial Advisor Section
        st.markdown("### AI Financial Advisor")
        
        st.markdown("""
        **Feature Overview:**
        
        The dashboard includes an AI-powered financial advisor that allows users to ask natural language questions about their financial data. The advisor can:
        
        - Answer questions about spending patterns and categories
        - Provide insights on income and savings
        - Analyze trends and monthly comparisons
        - Offer personalized financial advice based on transaction data
        
        **Implementation:**
        
        - **Rule-based System**: Keyword matching for common financial questions
        - **AI Integration**: Optional Google Gemini API integration for advanced natural language understanding
        - **Chat Interface**: Streamlit's chat components for conversational interaction
        - **Context-Aware**: Responses are based on filtered data, respecting sidebar filters
        - **Fallback Handling**: Default responses when questions are not understood
        
        **Design Choice**: The AI advisor is positioned as the 5th tab, before Methodology, to provide easy access to interactive querying while keeping documentation accessible at the end.
        """)
        
        # Methodology Summary
        st.markdown("### Methodology Summary")
        
        st.markdown("""
        This dashboard follows **Munzner's Nested Model for Visualization Design**:
        
        1. **Domain Problem**: Personal finance management, understanding spending patterns
        2. **Data/Task Abstraction**: Temporal, categorical, quantitative, geographic data; identify, compare, summarize tasks
        3. **Visual Encoding**: Position, color, size encodings chosen based on data types and accuracy requirements
        4. **Algorithm**: Efficient data processing, caching, real-time updates
        
        **Design Principles**: 
        - Clarity over complexity
        - User-centric design (personal use case)
        - Data-driven insights
        - Accessibility (high contrast, clear labels)
        - Performance optimization (caching, efficient queries)
        
        **Design Process**: Iterative development with user testing, spacing adjustments, visualization refinement based on 
        actual usage patterns and feedback.
        """)

else:
    st.error("Unable to load data. Please check if the data file exists.")
