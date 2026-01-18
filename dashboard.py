import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .positive {
        color: #10b981;
    }
    .negative {
        color: #ef4444;
    }
    </style>
""", unsafe_allow_html=True)

# Configuration: Set to 'real' or 'dummy' to switch datasets
# For public deployment, use 'dummy' to protect privacy
DATA_SOURCE = 'dummy'  # Change to 'real' for your actual data

# Load data
@st.cache_data
def load_data():
    # Select data file based on configuration
    if DATA_SOURCE == 'dummy':
        data_file = 'Dataset - Dummy Data.csv'
    else:
        data_file = 'Dataset - Sara Saad.csv'
    
    try:
        df = pd.read_csv(data_file)
        # Convert date columns to datetime
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        # Ensure Amount is numeric
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
        df['Amount_Abs'] = pd.to_numeric(df['Amount_Abs'], errors='coerce')
        # Add Country and City columns if they don't exist (for backward compatibility)
        if 'Country' not in df.columns:
            df['Country'] = 'Unknown'
        if 'City' not in df.columns:
            df['City'] = 'Unknown'
        return df
    except FileNotFoundError:
        # Try fallback to other file
        try:
            fallback_file = 'Dataset - Dummy Data.csv' if DATA_SOURCE == 'real' else 'Dataset - Sara Saad.csv'
            df = pd.read_csv(fallback_file)
            df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
            df['Amount_Abs'] = pd.to_numeric(df['Amount_Abs'], errors='coerce')
            # Add Country and City columns if they don't exist (for backward compatibility)
            if 'Country' not in df.columns:
                df['Country'] = 'Unknown'
            if 'City' not in df.columns:
                df['City'] = 'Unknown'
            st.info(f"⚠️ Using fallback data file: {fallback_file}")
            return df
        except Exception as e2:
            st.error(f"Error: Could not find data file. Please ensure '{data_file}' or '{fallback_file}' exists.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

if df is not None:
    # Header
    st.markdown('<h1 class="main-header">💰 Financial Dashboard</h1>', unsafe_allow_html=True)
    data_source_badge = "🔒 Dummy Data" if DATA_SOURCE == 'dummy' else "📊 Real Data"
    st.markdown(f'<p class="subtitle">Interactive Transaction Analytics & Insights | {data_source_badge}</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Year filter
    years = ['All'] + sorted(df['Year'].unique().tolist())
    selected_year = st.sidebar.selectbox("Select Year", years)
    
    # Product filter
    products = ['All'] + sorted(df['Product'].unique().tolist())
    selected_product = st.sidebar.selectbox("Select Product", products)
    
    # Transaction type filter
    types = ['All'] + sorted(df['Type'].unique().tolist())
    selected_type = st.sidebar.selectbox("Select Transaction Type", types)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Type'] == selected_type]
    
    # Calculate metrics
    current_balance = filtered_df['Balance'].iloc[-1] if len(filtered_df) > 0 else 0
    total_income = filtered_df[filtered_df['Amount'] > 0]['Amount'].sum()
    total_expenses = abs(filtered_df[filtered_df['Amount'] < 0]['Amount'].sum())
    net_flow = total_income - total_expenses
    expenses_df = filtered_df[filtered_df['Amount'] < 0].copy()
    income_df = filtered_df[filtered_df['Amount'] > 0].copy()
    
    # Additional metrics
    avg_daily_spending = total_expenses / max(len(filtered_df['Date'].unique()), 1) if len(filtered_df) > 0 else 0
    savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
    num_transactions = len(filtered_df)
    avg_transaction = filtered_df['Amount_Abs'].mean()
    
    # Calculate monthly summary (used across multiple tabs)
    monthly_df = filtered_df.copy()
    monthly_df['YearMonth'] = monthly_df['Date'].dt.to_period('M').astype(str)
    income_monthly = monthly_df[monthly_df['Amount'] > 0].groupby('YearMonth')['Amount'].sum().reset_index()
    income_monthly.columns = ['Month', 'Income']
    expenses_monthly = monthly_df[monthly_df['Amount'] < 0].groupby('YearMonth')['Amount_Abs'].sum().reset_index()
    expenses_monthly.columns = ['Month', 'Expenses']
    monthly_summary = pd.merge(income_monthly, expenses_monthly, on='Month', how='outer').fillna(0)
    monthly_summary = monthly_summary.sort_values('Month')
    monthly_summary['Net'] = monthly_summary['Income'] - monthly_summary['Expenses']
    
    # Weekday mapping for visualizations
    weekday_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 
                   'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    
    # Display key metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Current Balance", f"€{current_balance:,.2f}")
    
    with col2:
        st.metric("Total Income", f"€{total_income:,.2f}")
    
    with col3:
        st.metric("Total Expenses", f"€{total_expenses:,.2f}")
    
    with col4:
        delta_color = "normal" if net_flow >= 0 else "inverse"
        st.metric("Net Flow", f"€{net_flow:,.2f}", delta=f"€{net_flow:,.2f}", delta_color=delta_color)
    
    with col5:
        st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    with col6:
        st.metric("Avg Daily Spending", f"€{avg_daily_spending:,.2f}")
    
    st.divider()
    
    # Key Insights Section
    st.subheader("💡 Key Insights")
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        if len(expenses_df) > 0:
            top_category = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().idxmax()
            top_category_amount = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().max()
            st.info(f"**Top Spending Category**: {top_category}\n\n**Amount**: €{top_category_amount:,.2f}")
    
    with insight_col2:
        if len(filtered_df) > 0:
            date_range = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
            transactions_per_day = num_transactions / max(date_range, 1)
            st.info(f"**Transaction Frequency**: {transactions_per_day:.1f} transactions/day\n\n**Period**: {date_range} days")
    
    with insight_col3:
        if len(expenses_df) > 0:
            peak_hour = expenses_df.groupby('Hour')['Amount_Abs'].sum().idxmax()
            peak_hour_amount = expenses_df.groupby('Hour')['Amount_Abs'].sum().max()
            st.info(f"**Peak Spending Hour**: {peak_hour}:00\n\n**Amount**: €{peak_hour_amount:,.2f}")
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Overview", "💰 Spending Analysis", "📈 Trends", "🌍 Country Comparison", "🔍 Deep Dive", "🎨 Advanced Visuals", "🗺️ World Map"])
    
    with tab1:
        # Overview Tab
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Balance Over Time")
            balance_df = filtered_df.groupby('Date')['Balance'].last().reset_index()
            balance_df = balance_df.sort_values('Date')
            fig_balance = px.line(
                balance_df, 
                x='Date', 
                y='Balance',
                title="Account Balance Over Time",
                labels={'Balance': 'Balance (€)', 'Date': 'Date'},
                color_discrete_sequence=['#667eea']
            )
            fig_balance.add_hline(y=current_balance, line_dash="dash", line_color="red", 
                                 annotation_text=f"Current: €{current_balance:,.2f}")
            fig_balance.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            st.plotly_chart(fig_balance, use_container_width=True)
            
            st.subheader("📊 Expenses by Category")
            if len(expenses_df) > 0:
                category_expenses = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
                category_expenses = category_expenses.sort_values('Amount_Abs', ascending=False).head(10)
                fig_category = px.pie(
                    category_expenses,
                    values='Amount_Abs',
                    names='Merchant_Category',
                    title="Top 10 Expense Categories",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_category.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_category, use_container_width=True)
            else:
                st.info("No expense data available for selected filters.")
        
        with col2:
            st.subheader("💸 Monthly Income vs Expenses")
            
            fig_monthly = go.Figure()
            fig_monthly.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Income'],
                name='Income',
                marker_color='#10b981'
            ))
            fig_monthly.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Expenses'],
                name='Expenses',
                marker_color='#ef4444'
            ))
            fig_monthly.add_trace(go.Scatter(
                x=monthly_summary['Month'],
                y=monthly_summary['Net'],
                name='Net Flow',
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig_monthly.update_layout(
                title="Monthly Income vs Expenses with Net Flow",
                xaxis_title="Month",
                yaxis_title="Amount (€)",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
            
            st.subheader("🔄 Transaction Types Distribution")
            type_counts = filtered_df['Type'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Count']
            fig_type = px.bar(
                type_counts,
                x='Type',
                y='Count',
                title="Transaction Types Distribution",
                labels={'Count': 'Number of Transactions', 'Type': 'Transaction Type'},
                color='Count',
                color_continuous_scale='Viridis'
            )
            fig_type.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_type, use_container_width=True)
        
        # Product Comparison
        st.subheader("💳 Product Comparison")
        product_income = filtered_df[filtered_df['Amount'] > 0].groupby('Product')['Amount'].sum().reset_index()
        product_income.columns = ['Product', 'Income']
        
        product_expenses = filtered_df[filtered_df['Amount'] < 0].groupby('Product')['Amount_Abs'].sum().reset_index()
        product_expenses.columns = ['Product', 'Expenses']
        
        product_comparison = pd.merge(product_income, product_expenses, on='Product', how='outer').fillna(0)
        product_comparison['Net'] = product_comparison['Income'] - product_comparison['Expenses']
        
        fig_product = px.bar(
            product_comparison,
            x='Product',
            y=['Income', 'Expenses', 'Net'],
            title="Financial Activity by Product Type",
            barmode='group',
            color_discrete_map={'Income': '#10b981', 'Expenses': '#ef4444', 'Net': '#667eea'}
        )
        fig_product.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Amount (€)"
        )
        st.plotly_chart(fig_product, use_container_width=True)
        
        st.divider()
        
        # Additional Overview Visualizations
        # Row 1: Country Overview (if available) and Top Merchants
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Country' in filtered_df.columns and filtered_df['Country'].nunique() > 1:
                st.markdown("### 🌍 Spending by Country")
                country_spending = expenses_df.groupby('Country')['Amount_Abs'].sum().reset_index() if len(expenses_df) > 0 else pd.DataFrame()
                if len(country_spending) > 0:
                    country_spending = country_spending.sort_values('Amount_Abs', ascending=False)
                    fig_country_overview = px.bar(
                        country_spending,
                        x='Country',
                        y='Amount_Abs',
                        title="Total Spending by Country",
                        labels={'Amount_Abs': 'Spending (€)', 'Country': 'Country'},
                        color='Amount_Abs',
                        color_continuous_scale='Reds'
                    )
                    fig_country_overview.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False
                    )
                    st.plotly_chart(fig_country_overview, use_container_width=True)
            
            st.markdown("### 📈 Income vs Expenses Trend")
            if len(monthly_summary) > 0:
                monthly_summary['Savings_Rate'] = (monthly_summary['Net'] / monthly_summary['Income'] * 100).replace([np.inf, -np.inf], 0)
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=monthly_summary['Month'],
                    y=monthly_summary['Income'],
                    name='Income',
                    mode='lines+markers',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=8)
                ))
                fig_trend.add_trace(go.Scatter(
                    x=monthly_summary['Month'],
                    y=monthly_summary['Expenses'],
                    name='Expenses',
                    mode='lines+markers',
                    line=dict(color='#ef4444', width=3),
                    marker=dict(size=8)
                ))
                fig_trend.update_layout(
                    title="Income vs Expenses Trend Lines",
                    xaxis_title="Month",
                    yaxis_title="Amount (€)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            st.markdown("### 🏪 Top Spending Locations")
            if len(expenses_df) > 0:
                top_merchants = expenses_df.groupby('Description_Anon')['Amount_Abs'].sum().reset_index()
                top_merchants = top_merchants.sort_values('Amount_Abs', ascending=False).head(10)
                top_merchants.columns = ['Merchant', 'Total Spent']
                
                fig_merchants = px.bar(
                    top_merchants,
                    x='Total Spent',
                    y='Merchant',
                    orientation='h',
                    title="Top 10 Spending Locations",
                    labels={'Total Spent': 'Total Spent (€)', 'Merchant': 'Merchant'},
                    color='Total Spent',
                    color_continuous_scale='Blues'
                )
                fig_merchants.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_merchants, use_container_width=True)
            
            st.markdown("### 📊 Category Spending (Bar Chart)")
            if len(expenses_df) > 0:
                category_bar = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
                category_bar = category_bar.sort_values('Amount_Abs', ascending=False).head(10)
                
                fig_category_bar = px.bar(
                    category_bar,
                    x='Merchant_Category',
                    y='Amount_Abs',
                    title="Top 10 Categories by Spending",
                    labels={'Amount_Abs': 'Spending (€)', 'Merchant_Category': 'Category'},
                    color='Amount_Abs',
                    color_continuous_scale='Greens'
                )
                fig_category_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_category_bar, use_container_width=True)
        
        # Row 2: Financial Health Indicators and Activity Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💎 Financial Health Score")
            if total_income > 0:
                health_score = min(100, max(0, savings_rate + 50))
                health_color = "#10b981" if health_score >= 70 else "#f59e0b" if health_score >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {health_color}15 0%, {health_color}05 100%); border-radius: 10px; border: 2px solid {health_color};">
                    <h2 style="color: {health_color}; font-size: 3em; margin: 0;">{health_score:.0f}/100</h2>
                    <p style="color: #666; margin-top: 10px;">Based on savings rate and spending patterns</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📅 Activity Summary")
            date_range_days = (filtered_df['Date'].max() - filtered_df['Date'].min()).days if len(filtered_df) > 0 else 0
            transactions_per_day = num_transactions / max(date_range_days, 1)
            avg_daily_income = total_income / max(date_range_days, 1) if date_range_days > 0 else 0
            avg_daily_expenses = total_expenses / max(date_range_days, 1) if date_range_days > 0 else 0
            
            st.metric("Period", f"{date_range_days} days")
            st.metric("Transactions/Day", f"{transactions_per_day:.2f}")
            st.metric("Avg Daily Income", f"€{avg_daily_income:,.2f}")
            st.metric("Avg Daily Expenses", f"€{avg_daily_expenses:,.2f}")
        
        with col3:
            st.markdown("### 🎯 Spending Insights")
            if len(expenses_df) > 0:
                largest_expense = expenses_df['Amount_Abs'].max()
                avg_expense = expenses_df['Amount_Abs'].mean()
                median_expense = expenses_df['Amount_Abs'].median()
                
                st.metric("Largest Single Expense", f"€{largest_expense:,.2f}")
                st.metric("Average Expense", f"€{avg_expense:,.2f}")
                st.metric("Median Expense", f"€{median_expense:,.2f}")
                st.metric("Expense Transactions", f"{len(expenses_df)}")
        
        # Row 3: Cumulative Charts
        st.subheader("📈 Cumulative Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Cumulative Income Over Time")
            if len(income_df) > 0:
                income_sorted = income_df.sort_values('Date')
                income_sorted['Cumulative_Income'] = income_sorted['Amount'].cumsum()
                
                fig_cum_income = px.area(
                    income_sorted,
                    x='Date',
                    y='Cumulative_Income',
                    title="Cumulative Income Over Time",
                    labels={'Cumulative_Income': 'Cumulative Income (€)', 'Date': 'Date'},
                    color_discrete_sequence=['#10b981']
                )
                fig_cum_income.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_cum_income, use_container_width=True)
        
        with col2:
            st.markdown("### 💸 Cumulative Expenses Over Time")
            if len(expenses_df) > 0:
                expenses_sorted = expenses_df.sort_values('Date')
                expenses_sorted['Cumulative_Expenses'] = expenses_sorted['Amount_Abs'].cumsum()
                
                fig_cum_expenses = px.area(
                    expenses_sorted,
                    x='Date',
                    y='Cumulative_Expenses',
                    title="Cumulative Expenses Over Time",
                    labels={'Cumulative_Expenses': 'Cumulative Expenses (€)', 'Date': 'Date'},
                    color_discrete_sequence=['#ef4444']
                )
                fig_cum_expenses.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_cum_expenses, use_container_width=True)
        
        # Row 4: Quick Stats Cards
        st.subheader("📊 Quick Statistics")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                <h3 style="margin: 0; font-size: 0.9em;">Total Transactions</h3>
                <h1 style="margin: 10px 0; font-size: 2.5em;">{}</h1>
            </div>
            """.format(num_transactions), unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                <h3 style="margin: 0; font-size: 0.9em;">Total Income</h3>
                <h1 style="margin: 10px 0; font-size: 2.5em;">€{:.0f}K</h1>
            </div>
            """.format(total_income/1000), unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                <h3 style="margin: 0; font-size: 0.9em;">Total Expenses</h3>
                <h1 style="margin: 10px 0; font-size: 2.5em;">€{:.0f}K</h1>
            </div>
            """.format(total_expenses/1000), unsafe_allow_html=True)
        
        with stat_col4:
            net_color = "#10b981" if net_flow >= 0 else "#ef4444"
            st.markdown("""
            <div style="background: linear-gradient(135deg, {} 0%, {} 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                <h3 style="margin: 0; font-size: 0.9em;">Net Flow</h3>
                <h1 style="margin: 10px 0; font-size: 2.5em;">€{:.0f}K</h1>
            </div>
            """.format(net_color, net_color, net_flow/1000), unsafe_allow_html=True)
    
    with tab2:
        # Spending Analysis Tab
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Spending by Day of Week")
            if len(expenses_df) > 0:
                weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_expenses = expenses_df.groupby('Weekday')['Amount_Abs'].sum().reset_index()
                weekday_expenses['Weekday'] = pd.Categorical(weekday_expenses['Weekday'], categories=weekday_order, ordered=True)
                weekday_expenses = weekday_expenses.sort_values('Weekday')
                
                fig_weekday = px.bar(
                    weekday_expenses,
                    x='Weekday',
                    y='Amount_Abs',
                    title="Total Spending by Day of Week",
                    labels={'Amount_Abs': 'Total Spending (€)', 'Weekday': 'Day of Week'},
                    color='Amount_Abs',
                    color_continuous_scale='Blues'
                )
                fig_weekday.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig_weekday, use_container_width=True)
            
            st.subheader("⏰ Spending by Hour of Day")
            if len(expenses_df) > 0:
                hour_expenses = expenses_df.groupby('Hour')['Amount_Abs'].sum().reset_index()
                hour_expenses = hour_expenses.sort_values('Hour')
                
                fig_hour = px.area(
                    hour_expenses,
                    x='Hour',
                    y='Amount_Abs',
                    title="Total Spending by Hour of Day",
                    labels={'Amount_Abs': 'Total Spending (€)', 'Hour': 'Hour (24h format)'},
                    color_discrete_sequence=['#764ba2']
                )
                fig_hour.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified',
                    xaxis=dict(tickmode='linear', dtick=2)
                )
                st.plotly_chart(fig_hour, use_container_width=True)
        
        with col2:
            st.subheader("🔥 Top Spending Locations")
            if len(expenses_df) > 0:
                # Get top merchants (using Description_Anon as merchant name)
                top_merchants = expenses_df.groupby('Description_Anon')['Amount_Abs'].sum().reset_index()
                top_merchants = top_merchants.sort_values('Amount_Abs', ascending=False).head(15)
                top_merchants.columns = ['Merchant', 'Total Spent']
                
                fig_merchants = px.bar(
                    top_merchants,
                    x='Total Spent',
                    y='Merchant',
                    orientation='h',
                    title="Top 15 Spending Locations",
                    labels={'Total Spent': 'Total Spent (€)', 'Merchant': 'Merchant'},
                    color='Total Spent',
                    color_continuous_scale='Reds'
                )
                fig_merchants.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_merchants, use_container_width=True)
            
            st.subheader("📊 Average Transaction by Category")
            if len(expenses_df) > 0:
                avg_by_category = expenses_df.groupby('Merchant_Category')['Amount_Abs'].agg(['mean', 'count']).reset_index()
                avg_by_category.columns = ['Category', 'Avg Amount', 'Count']
                avg_by_category = avg_by_category[avg_by_category['Count'] >= 3].sort_values('Avg Amount', ascending=False).head(10)
                
                fig_avg = px.bar(
                    avg_by_category,
                    x='Category',
                    y='Avg Amount',
                    title="Average Transaction Amount by Category (min 3 transactions)",
                    labels={'Avg Amount': 'Average Amount (€)', 'Category': 'Category'},
                    color='Avg Amount',
                    color_continuous_scale='Greens'
                )
                fig_avg.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_avg, use_container_width=True)
        
        # Spending Heatmap
        st.subheader("🗓️ Spending Heatmap: Day of Week vs Hour")
        if len(expenses_df) > 0:
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = expenses_df.groupby(['Weekday', 'Hour'])['Amount_Abs'].sum().reset_index()
            heatmap_data['Weekday'] = pd.Categorical(heatmap_data['Weekday'], categories=weekday_order, ordered=True)
            heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='Hour', values='Amount_Abs').fillna(0)
            
            fig_heatmap = px.imshow(
                heatmap_pivot,
                labels=dict(x="Hour of Day", y="Day of Week", color="Spending (€)"),
                title="Spending Patterns: When Do You Spend Most?",
                color_continuous_scale='YlOrRd',
                aspect="auto"
            )
            fig_heatmap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        # Trends Tab
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Cumulative Spending Over Time")
            if len(expenses_df) > 0:
                expenses_sorted = expenses_df.sort_values('Date')
                expenses_sorted['Cumulative'] = expenses_sorted['Amount_Abs'].cumsum()
                
                fig_cumulative = px.line(
                    expenses_sorted,
                    x='Date',
                    y='Cumulative',
                    title="Cumulative Spending Over Time",
                    labels={'Cumulative': 'Cumulative Spending (€)', 'Date': 'Date'},
                    color_discrete_sequence=['#ef4444']
                )
                fig_cumulative.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_cumulative, use_container_width=True)
            
            st.subheader("📊 Category Trends Over Time")
            if len(expenses_df) > 0:
                top_categories = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(5).index
                category_trends = expenses_df[expenses_df['Merchant_Category'].isin(top_categories)].copy()
                category_trends['YearMonth'] = category_trends['Date'].dt.to_period('M').astype(str)
                category_monthly = category_trends.groupby(['YearMonth', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                
                fig_trends = px.line(
                    category_monthly,
                    x='YearMonth',
                    y='Amount_Abs',
                    color='Merchant_Category',
                    title="Top 5 Categories: Monthly Spending Trends",
                    labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                    markers=True
                )
                fig_trends.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_trends, use_container_width=True)
        
        with col2:
            st.subheader("💹 Income Trends Over Time")
            if len(income_df) > 0:
                income_sorted = income_df.sort_values('Date')
                income_sorted['YearMonth'] = income_sorted['Date'].dt.to_period('M').astype(str)
                income_monthly = income_sorted.groupby('YearMonth')['Amount'].sum().reset_index()
                
                fig_income_trend = px.bar(
                    income_monthly,
                    x='YearMonth',
                    y='Amount',
                    title="Monthly Income Trends",
                    labels={'Amount': 'Income (€)', 'YearMonth': 'Month'},
                    color='Amount',
                    color_continuous_scale='Greens'
                )
                fig_income_trend.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_income_trend, use_container_width=True)
            
            st.subheader("📉 Spending Velocity (Transactions per Day)")
            if len(expenses_df) > 0:
                daily_transactions = expenses_df.groupby('Date').size().reset_index()
                daily_transactions.columns = ['Date', 'Transaction Count']
                daily_transactions = daily_transactions.sort_values('Date')
                
                fig_velocity = px.scatter(
                    daily_transactions,
                    x='Date',
                    y='Transaction Count',
                    title="Daily Transaction Frequency",
                    labels={'Transaction Count': 'Number of Transactions', 'Date': 'Date'},
                    color='Transaction Count',
                    color_continuous_scale='Blues',
                    size='Transaction Count'
                )
                fig_velocity.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_velocity, use_container_width=True)
        
        # Monthly Savings Rate
        st.subheader("💎 Monthly Savings Rate")
        if len(monthly_summary) > 0:
            monthly_summary['Savings_Rate'] = (monthly_summary['Net'] / monthly_summary['Income'] * 100).replace([np.inf, -np.inf], 0)
            
            fig_savings = go.Figure()
            fig_savings.add_trace(go.Bar(
                x=monthly_summary['Month'],
                y=monthly_summary['Savings_Rate'],
                name='Savings Rate (%)',
                marker_color='#667eea'
            ))
            fig_savings.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
            fig_savings.update_layout(
                title="Monthly Savings Rate (%)",
                xaxis_title="Month",
                yaxis_title="Savings Rate (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_savings, use_container_width=True)
    
    with tab4:
        # Country Comparison Tab
        st.subheader("🌍 Country Comparison Analysis")
        
        # Check if Country column exists
        if 'Country' not in filtered_df.columns:
            st.warning("⚠️ Country data not available. Please regenerate data with location information.")
        else:
            # Country Overview Metrics
            country_col1, country_col2, country_col3, country_col4 = st.columns(4)
            
            with country_col1:
                if len(filtered_df) > 0:
                    countries_visited = filtered_df['Country'].nunique() if 'Country' in filtered_df.columns else 0
                    st.metric("Countries Visited", countries_visited)
            
            with country_col2:
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    most_expensive_country = expenses_df.groupby('Country')['Amount_Abs'].sum().idxmax()
                    st.metric("Most Expensive Country", most_expensive_country)
            
            with country_col3:
                if len(filtered_df) > 0 and 'Country' in filtered_df.columns:
                    most_transactions_country = filtered_df['Country'].mode()[0] if len(filtered_df['Country'].mode()) > 0 else "N/A"
                    st.metric("Most Transactions", most_transactions_country)
            
            with country_col4:
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    avg_by_country = expenses_df.groupby('Country')['Amount_Abs'].mean()
                    highest_avg_country = avg_by_country.idxmax()
                    st.metric("Highest Avg Transaction", highest_avg_country)
            
            st.divider()
            
            # Row 1: Total Spending by Country
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💰 Total Spending by Country")
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    country_spending = expenses_df.groupby('Country')['Amount_Abs'].sum().reset_index()
                    country_spending = country_spending.sort_values('Amount_Abs', ascending=False)
                    
                    fig_country_bar = px.bar(
                        country_spending,
                        x='Country',
                        y='Amount_Abs',
                        title="Total Spending by Country",
                        labels={'Amount_Abs': 'Total Spending (€)', 'Country': 'Country'},
                        color='Amount_Abs',
                        color_continuous_scale='Reds'
                    )
                    fig_country_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False
                    )
                    st.plotly_chart(fig_country_bar, use_container_width=True)
                
                st.markdown("### 📊 Spending Distribution by Country")
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    country_pie = expenses_df.groupby('Country')['Amount_Abs'].sum().reset_index()
                    fig_country_pie = px.pie(
                        country_pie,
                        values='Amount_Abs',
                        names='Country',
                        title="Spending Distribution Across Countries",
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig_country_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_country_pie, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Monthly Spending Trends by Country")
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    expenses_df['YearMonth'] = expenses_df['Date'].dt.to_period('M').astype(str)
                    country_monthly = expenses_df.groupby(['YearMonth', 'Country'])['Amount_Abs'].sum().reset_index()
                    
                    fig_country_trend = px.line(
                        country_monthly,
                        x='YearMonth',
                        y='Amount_Abs',
                        color='Country',
                        title="Monthly Spending Trends by Country",
                        labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                        markers=True
                    )
                    fig_country_trend.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified',
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_country_trend, use_container_width=True)
                
                st.markdown("### 🏙️ Spending by City")
                if len(expenses_df) > 0 and 'City' in expenses_df.columns:
                    city_spending = expenses_df.groupby('City')['Amount_Abs'].sum().reset_index()
                    city_spending = city_spending.sort_values('Amount_Abs', ascending=False)
                    
                    fig_city = px.bar(
                        city_spending,
                        x='City',
                        y='Amount_Abs',
                        title="Total Spending by City",
                        labels={'Amount_Abs': 'Total Spending (€)', 'City': 'City'},
                        color='Amount_Abs',
                        color_continuous_scale='Blues'
                    )
                    fig_city.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False
                    )
                    st.plotly_chart(fig_city, use_container_width=True)
            
            # Row 2: Category Comparison by Country
            st.markdown("### 🛍️ Spending Categories by Country")
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_category = expenses_df.groupby(['Country', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                country_category_pivot = country_category.pivot(index='Merchant_Category', columns='Country', values='Amount_Abs').fillna(0)
                
                fig_category_country = px.bar(
                    country_category.reset_index(),
                    x='Merchant_Category',
                    y='Amount_Abs',
                    color='Country',
                    title="Spending Categories Comparison Across Countries",
                    labels={'Amount_Abs': 'Spending (€)', 'Merchant_Category': 'Category'},
                    barmode='group'
                )
                fig_category_country.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_category_country, use_container_width=True)
            
            # Row 3: Heatmap and Box Plot
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔥 Spending Heatmap: Country vs Category")
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    heatmap_country = expenses_df.groupby(['Country', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
                    heatmap_pivot = heatmap_country.pivot(index='Merchant_Category', columns='Country', values='Amount_Abs').fillna(0)
                    
                    fig_heatmap_country = px.imshow(
                        heatmap_pivot,
                        labels=dict(x="Country", y="Category", color="Spending (€)"),
                        title="Spending Heatmap: Country vs Category",
                        color_continuous_scale='YlOrRd',
                        aspect="auto"
                    )
                    fig_heatmap_country.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_heatmap_country, use_container_width=True)
            
            with col2:
                st.markdown("### 📦 Transaction Amount Distribution by Country")
                if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                    fig_box_country = px.box(
                        expenses_df,
                        x='Country',
                        y='Amount_Abs',
                        title="Transaction Amount Distribution by Country",
                        labels={'Amount_Abs': 'Amount (€)', 'Country': 'Country'},
                        color='Country'
                    )
                    fig_box_country.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False
                    )
                    st.plotly_chart(fig_box_country, use_container_width=True)
            
            # Row 4: Advanced Comparisons
            st.markdown("### 📊 Country Statistics Comparison")
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_stats = expenses_df.groupby('Country').agg({
                    'Amount_Abs': ['sum', 'mean', 'median', 'count', 'std']
                }).reset_index()
                country_stats.columns = ['Country', 'Total', 'Average', 'Median', 'Count', 'Std Dev']
                country_stats = country_stats.sort_values('Total', ascending=False)
                country_stats['Total'] = country_stats['Total'].apply(lambda x: f"€{x:,.2f}")
                country_stats['Average'] = country_stats['Average'].apply(lambda x: f"€{x:,.2f}")
                country_stats['Median'] = country_stats['Median'].apply(lambda x: f"€{x:,.2f}")
                country_stats['Std Dev'] = country_stats['Std Dev'].apply(lambda x: f"€{x:,.2f}")
                
                st.dataframe(country_stats, use_container_width=True, hide_index=True)
            
            # Row 5: Timeline Visualization
            st.markdown("### 📅 Country Timeline & Spending")
            if len(filtered_df) > 0 and 'Country' in filtered_df.columns:
                timeline_df = filtered_df[filtered_df['Amount'] < 0].copy() if len(filtered_df[filtered_df['Amount'] < 0]) > 0 else filtered_df.copy()
                timeline_df['YearMonth'] = timeline_df['Date'].dt.to_period('M').astype(str)
                
                # Create stacked area chart showing country presence over time
                country_timeline = timeline_df.groupby(['YearMonth', 'Country']).size().reset_index(name='Transaction_Count')
                
                fig_timeline = px.area(
                    country_timeline,
                    x='YearMonth',
                    y='Transaction_Count',
                    color='Country',
                    title="Country Presence Timeline (Transaction Count)",
                    labels={'Transaction_Count': 'Number of Transactions', 'YearMonth': 'Month'},
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_timeline.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab5:
        # Deep Dive Tab - Detailed Analysis
        st.subheader("🔍 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Spending Statistics")
            if len(expenses_df) > 0:
                stats_data = {
                    'Metric': [
                        'Total Expenses',
                        'Average Transaction',
                        'Median Transaction',
                        'Largest Single Expense',
                        'Smallest Expense',
                        'Standard Deviation',
                        'Total Transactions'
                    ],
                    'Value': [
                        f"€{total_expenses:,.2f}",
                        f"€{expenses_df['Amount_Abs'].mean():,.2f}",
                        f"€{expenses_df['Amount_Abs'].median():,.2f}",
                        f"€{expenses_df['Amount_Abs'].max():,.2f}",
                        f"€{expenses_df['Amount_Abs'].min():,.2f}",
                        f"€{expenses_df['Amount_Abs'].std():,.2f}",
                        f"{len(expenses_df)}"
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 💰 Income Statistics")
            if len(income_df) > 0:
                income_stats_data = {
                    'Metric': [
                        'Total Income',
                        'Average Income Transaction',
                        'Median Income Transaction',
                        'Largest Single Income',
                        'Smallest Income',
                        'Standard Deviation',
                        'Total Income Transactions'
                    ],
                    'Value': [
                        f"€{total_income:,.2f}",
                        f"€{income_df['Amount'].mean():,.2f}",
                        f"€{income_df['Amount'].median():,.2f}",
                        f"€{income_df['Amount'].max():,.2f}",
                        f"€{income_df['Amount'].min():,.2f}",
                        f"€{income_df['Amount'].std():,.2f}",
                        f"{len(income_df)}"
                    ]
                }
                income_stats_df = pd.DataFrame(income_stats_data)
                st.dataframe(income_stats_df, use_container_width=True, hide_index=True)
        
        # Category Breakdown Table
        st.subheader("📋 Detailed Category Breakdown")
        if len(expenses_df) > 0:
            category_breakdown = expenses_df.groupby('Merchant_Category').agg({
                'Amount_Abs': ['sum', 'mean', 'count', 'min', 'max']
            }).reset_index()
            category_breakdown.columns = ['Category', 'Total', 'Average', 'Count', 'Min', 'Max']
            category_breakdown = category_breakdown.sort_values('Total', ascending=False)
            category_breakdown['Total'] = category_breakdown['Total'].apply(lambda x: f"€{x:,.2f}")
            category_breakdown['Average'] = category_breakdown['Average'].apply(lambda x: f"€{x:,.2f}")
            category_breakdown['Min'] = category_breakdown['Min'].apply(lambda x: f"€{x:,.2f}")
            category_breakdown['Max'] = category_breakdown['Max'].apply(lambda x: f"€{x:,.2f}")
            
            st.dataframe(category_breakdown, use_container_width=True, hide_index=True)
        
        # Transaction table
        st.subheader("📋 Recent Transactions")
        
        if len(filtered_df) > 0:
            num_rows = 50  # Fixed number of recent transactions to display
            # Ensure Date column exists and is datetime
            if 'Date' not in filtered_df.columns:
                filtered_df['Date'] = pd.to_datetime(filtered_df[['Year', 'Month', 'Day']])
            
            display_df = filtered_df.sort_values('Date', ascending=False).head(num_rows).copy()
            
            # Select columns that exist
            available_cols = ['Date', 'Type', 'Product', 'Merchant_Category', 'Amount', 'Balance']
            if 'Country' in display_df.columns:
                available_cols.insert(4, 'Country')
            if 'City' in display_df.columns:
                available_cols.insert(5, 'City')
            
            display_df = display_df[[col for col in available_cols if col in display_df.columns]].copy()
            
            # Format Date column
            if 'Date' in display_df.columns:
                display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
            
            # Format Amount and Balance
            if 'Amount' in display_df.columns:
                display_df['Amount'] = display_df['Amount'].apply(lambda x: f"€{float(x):,.2f}" if pd.notna(x) else "€0.00")
            if 'Balance' in display_df.columns:
                display_df['Balance'] = display_df['Balance'].apply(lambda x: f"€{float(x):,.2f}" if pd.notna(x) else "€0.00")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
        else:
            st.info("No transactions available for the selected filters.")
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"filtered_transactions_{selected_year}_{selected_product}_{selected_type}.csv",
            mime="text/csv"
        )
    
    with tab6:
        # Advanced Visuals Tab
        st.subheader("🎨 Advanced Visualizations")
        
        # Row 1: Box plots and Violin plots
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📦 Transaction Amount Distribution by Category")
            if len(expenses_df) > 0:
                top_cats = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(8).index
                expenses_filtered = expenses_df[expenses_df['Merchant_Category'].isin(top_cats)]
                fig_box = px.box(
                    expenses_filtered,
                    x='Merchant_Category',
                    y='Amount_Abs',
                    title="Transaction Amount Distribution (Top 8 Categories)",
                    labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                    color='Merchant_Category'
                )
                fig_box.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                st.plotly_chart(fig_box, use_container_width=True)
            
            st.markdown("### 🎯 Scatter: Transaction Size vs Balance")
            if len(filtered_df) > 0:
                scatter_df = filtered_df[filtered_df['Amount'] != 0].copy()
                scatter_df['Transaction_Type'] = scatter_df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
                fig_scatter = px.scatter(
                    scatter_df.head(500),  # Limit for performance
                    x='Amount_Abs',
                    y='Balance',
                    color='Transaction_Type',
                    size='Amount_Abs',
                    hover_data=['Merchant_Category', 'Date'],
                    title="Transaction Size vs Account Balance",
                    labels={'Amount_Abs': 'Transaction Amount (€)', 'Balance': 'Account Balance (€)'},
                    color_discrete_map={'Income': '#10b981', 'Expense': '#ef4444'}
                )
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.markdown("### 🎻 Violin Plot: Spending Distribution")
            if len(expenses_df) > 0:
                top_cats_violin = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(6).index
                expenses_violin = expenses_df[expenses_df['Merchant_Category'].isin(top_cats_violin)]
                fig_violin = px.violin(
                    expenses_violin,
                    x='Merchant_Category',
                    y='Amount_Abs',
                    title="Spending Distribution (Violin Plot)",
                    labels={'Amount_Abs': 'Amount (€)', 'Merchant_Category': 'Category'},
                    color='Merchant_Category',
                    box=True
                )
                fig_violin.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                st.plotly_chart(fig_violin, use_container_width=True)
            
            st.markdown("### 📊 Funnel Chart: Transaction Flow")
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
                    title="Transaction Type Funnel",
                    labels={'Count': 'Number of Transactions', 'Stage': 'Transaction Type'}
                )
                fig_funnel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Row 2: Sunburst and Treemap
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ☀️ Sunburst: Product → Category → Type")
            if len(filtered_df) > 0:
                sunburst_data = filtered_df.groupby(['Product', 'Merchant_Category', 'Type']).size().reset_index(name='Count')
                sunburst_data = sunburst_data[sunburst_data['Count'] > 0]
                fig_sunburst = px.sunburst(
                    sunburst_data,
                    path=['Product', 'Merchant_Category', 'Type'],
                    values='Count',
                    title="Hierarchical View: Product → Category → Type",
                    color='Count',
                    color_continuous_scale='Viridis'
                )
                fig_sunburst.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_sunburst, use_container_width=True)
        
        with col2:
            st.markdown("### 🌳 Treemap: Category Spending")
            if len(expenses_df) > 0:
                treemap_data = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().reset_index()
                treemap_data = treemap_data.sort_values('Amount_Abs', ascending=False)
                fig_treemap = px.treemap(
                    treemap_data,
                    path=['Merchant_Category'],
                    values='Amount_Abs',
                    title="Spending Treemap by Category",
                    color='Amount_Abs',
                    color_continuous_scale='Reds'
                )
                fig_treemap.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Row 3: Waterfall and Gauge
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💧 Waterfall: Monthly Net Flow")
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
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                ))
                fig_waterfall.update_layout(
                    title="Monthly Net Flow Waterfall Chart",
                    xaxis_title="Month",
                    yaxis_title="Net Flow (€)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig_waterfall, use_container_width=True)
        
        with col2:
            st.markdown("### 🎚️ Gauge: Financial Health")
            # Calculate financial health score (0-100)
            if total_income > 0:
                health_score = min(100, max(0, (savings_rate + 50)))  # Normalize to 0-100
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=health_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Financial Health Score"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 33], 'color': "lightgray"},
                            {'range': [33, 66], 'color': "gray"},
                            {'range': [66, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=300
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Row 4: Radar/Spider and Parallel Coordinates
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🕸️ Radar Chart: Spending by Day of Week")
            if len(expenses_df) > 0:
                weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_spending = expenses_df.groupby('Weekday')['Amount_Abs'].sum().reset_index()
                
                # Ensure all weekdays are present
                all_weekdays_df = pd.DataFrame({'Weekday': weekday_order})
                weekday_spending = pd.merge(all_weekdays_df, weekday_spending, on='Weekday', how='left')
                weekday_spending['Amount_Abs'] = weekday_spending['Amount_Abs'].fillna(0)
                weekday_spending['Weekday'] = pd.Categorical(weekday_spending['Weekday'], categories=weekday_order, ordered=True)
                weekday_spending = weekday_spending.sort_values('Weekday')
                
                # Normalize for radar chart
                max_val = weekday_spending['Amount_Abs'].max()
                if max_val > 0:
                    weekday_spending['Normalized'] = (weekday_spending['Amount_Abs'] / max_val * 100)
                else:
                    weekday_spending['Normalized'] = 0
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=weekday_spending['Normalized'].tolist(),
                    theta=weekday_spending['Weekday'].tolist(),
                    fill='toself',
                    name='Spending Pattern',
                    line_color='#667eea'
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title="Spending Pattern by Day of Week (Radar)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Parallel Coordinates: Multi-Dimensional Analysis")
            if len(expenses_df) > 0:
                # Sample data for parallel coordinates
                parallel_data = expenses_df[['Amount_Abs', 'Hour', 'Weekday', 'Merchant_Category']].copy()
                parallel_data = parallel_data.head(200)  # Limit for performance
                
                # Convert weekday to numeric
                weekday_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 
                              'Friday': 5, 'Saturday': 6, 'Sunday': 7}
                parallel_data['Weekday_Num'] = parallel_data['Weekday'].map(weekday_map)
                
                # Get top categories
                top_cats_parallel = parallel_data['Merchant_Category'].value_counts().head(5).index
                parallel_data = parallel_data[parallel_data['Merchant_Category'].isin(top_cats_parallel)]
                
                fig_parallel = px.parallel_coordinates(
                    parallel_data,
                    color='Amount_Abs',
                    dimensions=['Amount_Abs', 'Hour', 'Weekday_Num'],
                    labels={'Amount_Abs': 'Amount', 'Hour': 'Hour', 'Weekday_Num': 'Day'},
                    color_continuous_scale='Viridis',
                    title="Multi-Dimensional Transaction Analysis"
                )
                fig_parallel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_parallel, use_container_width=True)
        
        # Row 5: 3D Scatter and Surface
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌐 3D Scatter: Amount vs Hour vs Day")
            if len(expenses_df) > 0:
                scatter_3d_data = expenses_df.head(300).copy()  # Limit for performance
                scatter_3d_data['Weekday_Num'] = scatter_3d_data['Weekday'].map(weekday_map)
                
                fig_3d = px.scatter_3d(
                    scatter_3d_data,
                    x='Hour',
                    y='Weekday_Num',
                    z='Amount_Abs',
                    color='Merchant_Category',
                    size='Amount_Abs',
                    hover_data=['Date'],
                    title="3D View: Spending Patterns",
                    labels={'Hour': 'Hour of Day', 'Weekday_Num': 'Day of Week', 'Amount_Abs': 'Amount (€)'}
                )
                fig_3d.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    scene=dict(
                        xaxis_title="Hour",
                        yaxis_title="Day of Week",
                        zaxis_title="Amount (€)"
                    )
                )
                st.plotly_chart(fig_3d, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Histogram: Transaction Amount Distribution")
            if len(filtered_df) > 0:
                fig_hist = px.histogram(
                    filtered_df,
                    x='Amount_Abs',
                    nbins=50,
                    title="Distribution of Transaction Amounts",
                    labels={'Amount_Abs': 'Transaction Amount (€)', 'count': 'Frequency'},
                    color_discrete_sequence=['#667eea'],
                    marginal="box"
                )
                fig_hist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        # Row 6: Additional visualizations
        st.markdown("### 📉 Stacked Area: Category Trends Over Time")
        if len(expenses_df) > 0:
            expenses_df['YearMonth'] = expenses_df['Date'].dt.to_period('M').astype(str)
            top_cats_area = expenses_df.groupby('Merchant_Category')['Amount_Abs'].sum().nlargest(6).index
            area_data = expenses_df[expenses_df['Merchant_Category'].isin(top_cats_area)]
            area_monthly = area_data.groupby(['YearMonth', 'Merchant_Category'])['Amount_Abs'].sum().reset_index()
            
            fig_area = px.area(
                area_monthly,
                x='YearMonth',
                y='Amount_Abs',
                color='Merchant_Category',
                title="Stacked Area: Top 6 Categories Over Time",
                labels={'Amount_Abs': 'Spending (€)', 'YearMonth': 'Month'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_area.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_area, use_container_width=True)
    
    with tab7:
        # World Map Tab
        st.subheader("🗺️ World Map - Spending by Country")
        
        if 'Country' not in filtered_df.columns:
            st.warning("⚠️ Country data not available. Please regenerate data with location information.")
        else:
            # Country to ISO code mapping
            country_iso_map = {
                'Belgium': 'BEL',
                'Spain': 'ESP',
                'Germany': 'DEU',
                'France': 'FRA',
                'Unknown': None
            }
            
            # Prepare data for map
            if len(expenses_df) > 0 and 'Country' in expenses_df.columns:
                country_data = expenses_df.groupby('Country').agg({
                    'Amount_Abs': ['sum', 'mean', 'count']
                }).reset_index()
                country_data.columns = ['Country', 'Total_Spending', 'Avg_Spending', 'Transaction_Count']
                country_data['ISO_Code'] = country_data['Country'].map(country_iso_map)
                country_data = country_data[country_data['ISO_Code'].notna()]  # Remove Unknown countries
                
                # Get city data for statistics
                city_data = expenses_df.groupby(['Country', 'City']).agg({
                    'Amount_Abs': 'sum'
                }).reset_index()
                city_data.columns = ['Country', 'City', 'Spending']
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Choropleth map for country-level spending
                    st.markdown("### 🌍 Spending by Country (Choropleth)")
                    if len(country_data) > 0:
                        fig_choropleth = go.Figure(data=go.Choropleth(
                            locations=country_data['ISO_Code'],
                            z=country_data['Total_Spending'],
                            text=country_data['Country'],
                            locationmode='ISO-3',
                            colorscale='Reds',
                            autocolorscale=False,
                            reversescale=False,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_title="Total Spending (€)",
                            hovertemplate='<b>%{text}</b><br>' +
                                        'Total Spending: €%{z:,.2f}<br>' +
                                        '<extra></extra>'
                        ))
                        
                        fig_choropleth.update_geos(
                            projection_type="natural earth",
                            showcoastlines=True,
                            coastlinecolor="LightGray",
                            showland=True,
                            landcolor="White",
                            showocean=True,
                            oceancolor="LightBlue",
                            showlakes=True,
                            lakecolor="LightBlue",
                            showrivers=True,
                            rivercolor="LightBlue",
                            center=dict(lon=10, lat=50),  # Center on Europe
                            projection_scale=4,  # Zoom in on Europe
                            lonaxis_range=[-10, 40],  # Europe longitude range
                            lataxis_range=[35, 70]   # Europe latitude range
                        )
                        
                        fig_choropleth.update_layout(
                            title_text='Total Spending by Country - Europe Focus',
                            geo=dict(
                                showframe=False,
                                showcoastlines=True,
                                projection_type='natural earth',
                                center=dict(lon=10, lat=50),
                                projection_scale=4,
                                lonaxis_range=[-10, 40],
                                lataxis_range=[35, 70]
                            ),
                            height=600,
                            margin=dict(l=0, r=0, t=50, b=0)
                        )
                        
                        st.plotly_chart(fig_choropleth, use_container_width=True)
                    else:
                        st.warning("No country data available for mapping.")
                
                with col2:
                    st.markdown("### 📊 Country Statistics")
                    st.dataframe(
                        country_data[['Country', 'Total_Spending', 'Avg_Spending', 'Transaction_Count']].round(2),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.markdown("### 🏙️ City Statistics")
                    city_stats = city_data[['City', 'Country', 'Spending']].copy()
                    city_stats = city_stats.sort_values('Spending', ascending=False)
                    city_stats['Spending'] = city_stats['Spending'].apply(lambda x: f"€{x:,.2f}")
                    st.dataframe(
                        city_stats,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Map legend/info
                    st.markdown("### ℹ️ Map Information")
                    st.info("""
                    **Choropleth Map**: Shows total spending by country with color intensity. 
                    Darker colors indicate higher spending amounts.
                    
                    **Interactivity**: 
                    - Hover over countries for detailed spending information
                    - Zoom and pan to explore the map
                    - Color scale shows spending intensity
                    """)
            else:
                st.info("No expense data available for selected filters.")
    
    st.divider()
    
    # Summary Statistics
    st.subheader("📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Transactions", len(filtered_df))
        st.metric("Average Transaction", f"€{avg_transaction:,.2f}")
    
    with col2:
        largest_income = filtered_df[filtered_df['Amount'] > 0]['Amount'].max() if len(filtered_df[filtered_df['Amount'] > 0]) > 0 else 0
        largest_expense = filtered_df[filtered_df['Amount'] < 0]['Amount_Abs'].max() if len(filtered_df[filtered_df['Amount'] < 0]) > 0 else 0
        st.metric("Largest Income", f"€{largest_income:,.2f}" if largest_income > 0 else "€0.00")
        st.metric("Largest Expense", f"€{largest_expense:,.2f}" if largest_expense > 0 else "€0.00")
    
    with col3:
        most_active_category = filtered_df['Merchant_Category'].mode()[0] if len(filtered_df['Merchant_Category'].mode()) > 0 else "N/A"
        most_common_type = filtered_df['Type'].mode()[0] if len(filtered_df['Type'].mode()) > 0 else "N/A"
        st.metric("Most Active Category", most_active_category)
        st.metric("Most Common Type", most_common_type)
    
    with col4:
        date_range_days = (filtered_df['Date'].max() - filtered_df['Date'].min()).days if len(filtered_df) > 0 else 0
        st.metric("Date Range", f"{date_range_days} days")
        st.metric("Transactions/Day", f"{num_transactions/max(date_range_days, 1):.2f}")

else:
    st.error("Unable to load data. Please check if the data file exists in the current directory.")
