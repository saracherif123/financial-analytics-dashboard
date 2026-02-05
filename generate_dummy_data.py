"""
Generate dummy financial transaction data similar to the original dataset structure.
This creates realistic but fake data for public deployment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
# 20 months * ~35 transactions/month = ~700 transactions + 20 Topups = ~720 total
NUM_TRANSACTIONS = 720  # Realistic number for budget-conscious student
START_DATE = datetime(2024, 9, 1)  # Start of Erasmus Mundus program
END_DATE = datetime(2026, 5, 1)  # 20 months total (6+6+2+6)

# Country timeline for Erasmus Mundus program
# Timeline: Belgium 6 months, Spain 6 months, Germany 2 months, France 6 months
COUNTRY_TIMELINE = [
    {'country': 'Belgium', 'city': 'Brussels', 'start': datetime(2024, 9, 1), 'end': datetime(2025, 3, 1)},  # 6 months
    {'country': 'Spain', 'city': 'Barcelona', 'start': datetime(2025, 3, 1), 'end': datetime(2025, 9, 1)},  # 6 months
    {'country': 'Germany', 'city': 'Berlin', 'start': datetime(2025, 9, 1), 'end': datetime(2025, 11, 1)},  # 2 months
    {'country': 'France', 'city': 'Paris', 'start': datetime(2025, 11, 1), 'end': datetime(2026, 5, 1)},  # 6 months
]

# Country-specific merchant patterns
COUNTRY_MERCHANTS = {
    'Belgium': {
        'Food & Dining': ['Colruyt', 'Carrefour', 'Delhaize', 'Aldi', 'Fritland', 'Belgian Waffle House'],
        'Transportation': ['SNCB', 'STIB-MIVB', 'De Lijn', 'Bolt Brussels'],
        'Shopping & Retail': ['H&M Brussels', 'Zara Brussels', 'MediaMarkt'],
        'Other': ['Atomium Shop', 'Brussels Expo', 'Belgian Chocolate Shop']
    },
    'Spain': {
        'Food & Dining': ['Mercadona', 'Carrefour', 'Lidl', 'El Corte Inglés', 'Tapas Bar', 'Paella Restaurant'],
        'Transportation': ['Renfe', 'Metro Barcelona', 'Bolt Barcelona', 'Taxi Barcelona'],
        'Shopping & Retail': ['Zara Spain', 'Pull&Bear', 'Primark Barcelona'],
        'Other': ['Sagrada Familia Shop', 'Park Güell', 'Barcelona Museum']
    },
    'Germany': {
        'Food & Dining': ['REWE', 'EDEKA', 'Aldi', 'Lidl', 'Bakery Berlin', 'Currywurst Stand'],
        'Transportation': ['Deutsche Bahn', 'BVG Berlin', 'Bolt Berlin', 'S-Bahn'],
        'Shopping & Retail': ['H&M Berlin', 'Müller', 'DM Drogerie', 'Primark Berlin'],
        'Other': ['Berlin Museum', 'Brandenburg Gate Shop', 'Berlin Souvenirs']
    },
    'France': {
        'Food & Dining': ['Carrefour Paris', 'Monoprix', 'Franprix', 'Boulangerie', 'Café Parisien'],
        'Transportation': ['RATP', 'SNCF', 'Bolt Paris', 'Vélib'],
        'Shopping & Retail': ['Galeries Lafayette', 'Printemps', 'FNAC'],
        'Other': ['Louvre Shop', 'Eiffel Tower', 'Paris Souvenirs']
    }
}

# Transaction types and their probabilities
# Adjusted Topup frequency to target ~€1000/month average income
# With ~1000 transactions over 20 months = ~50 transactions/month
# Need ~1 Topup per month = 2% frequency
TRANSACTION_TYPES = {
    'Card Payment': 0.60,  # Most common - daily expenses
    'Transfer': 0.25,      # Bank transfers, rent payments
    'Topup': 0.02,         # ~1 per month = €1000/month income
    'Fee': 0.04,           # Banking fees, ATM fees
    'Reward': 0.03,        # Cashback, small rewards
    'Interest': 0.02,      # Savings interest
    'Card Refund': 0.02,   # Returns, refunds
    'Exchange': 0.02       # Currency exchange
}

# Products
PRODUCTS = ['Current', 'Savings', 'Deposit']

# Merchant categories (based on original data)
MERCHANT_CATEGORIES = [
    'Food & Dining',
    'Transfers & Payments',
    'Transportation',
    'Utilities & Bills',
    'Shopping & Retail',
    'Entertainment & Recreation',
    'Education',
    'Personal Care & Services',
    'Income & Deposits',
    'Fees & Charges',
    'Financial Services',
    'Other'
]

# Category-specific merchants (for Description_Anon)
MERCHANTS_BY_CATEGORY = {
    'Food & Dining': ['Restaurant ABC', 'Cafe XYZ', 'Fast Food Chain', 'Grocery Store', 'Bakery Shop', 'Coffee House'],
    'Transportation': ['Public Transit', 'Ride Share', 'Taxi Service', 'Train Company', 'Bus Service'],
    'Utilities & Bills': ['Electric Company', 'Water Utility', 'Internet Provider', 'Phone Company', 'Gas Company'],
    'Shopping & Retail': ['Department Store', 'Online Retailer', 'Clothing Store', 'Electronics Shop'],
    'Entertainment & Recreation': ['Cinema', 'Streaming Service', 'Gym Membership', 'Event Ticket'],
    'Education': ['University', 'Bookstore', 'Online Course', 'Student Services'],
    'Personal Care & Services': ['Hair Salon', 'Laundry Service', 'Spa', 'Dry Cleaner'],
    'Transfers & Payments': ['Bank Transfer', 'Pocket Withdrawal', 'Payment Received', 'Money Transfer'],
    'Income & Deposits': ['Salary Payment', 'Freelance Payment', 'Investment Return', 'Refund'],
    'Fees & Charges': ['Service Fee', 'Card Fee', 'Transaction Fee', 'Monthly Fee'],
    'Financial Services': ['Bank Interest', 'Investment', 'Savings Interest'],
    'Other': ['Miscellaneous', 'Unknown Merchant', 'Various Services']
}

# Amount ranges by transaction type (in euros)
# Realistic Erasmus Mundus student amounts - €1000/month income
AMOUNT_RANGES = {
    'Card Payment': (-80, -1),   # Daily expenses: groceries, coffee, transport
    'Transfer': (-600, 50),     # Rent, utilities, occasional transfers received
    'Topup': (950, 1050),       # Monthly Erasmus stipend/scholarship ~€1000
    'Fee': (-15, -1),           # Banking fees, ATM fees
    'Reward': (1, 5),           # Cashback, small rewards (reduced)
    'Interest': (0.1, 1),       # Savings interest (reduced)
    'Card Refund': (1, 80),     # Returns, refunds
    'Exchange': (-200, 200)     # Currency exchange between countries
}

# Hour distribution (more transactions during business hours)
HOUR_WEIGHTS = {
    0: 0.01, 1: 0.01, 2: 0.005, 3: 0.005, 4: 0.005, 5: 0.01,
    6: 0.02, 7: 0.03, 8: 0.04, 9: 0.05, 10: 0.06, 11: 0.07,
    12: 0.08, 13: 0.08, 14: 0.07, 15: 0.07, 16: 0.06, 17: 0.06,
    18: 0.08, 19: 0.07, 20: 0.05, 21: 0.04, 22: 0.03, 23: 0.02
}

def get_country_for_date(date, country_timeline):
    """Determine which country the person was in on a given date."""
    for period in country_timeline:
        if period['start'] <= date < period['end']:
            return period['country'], period['city']
    # Default to last country if date is beyond timeline
    return country_timeline[-1]['country'], country_timeline[-1]['city']

def generate_transactions(num_transactions, start_date, end_date):
    """Generate realistic transaction data."""
    transactions = []
    
    # Calculate date range
    date_range = (end_date - start_date).days
    
    # Initial balance (starting with first month's stipend + lump sum if September 2024)
    # Check if start_date is September 2024 - if so, add lump sum
    # Adjusted to get final balance around €2000-3000 (lower than €5000)
    if start_date.year == 2024 and start_date.month == 9:
        current_balance = 1500.0  # Reduced to get final balance around €2000-3000
    else:
        current_balance = 500.0  # Reduced initial balance
    
    # Generate dates with realistic distribution
    # Ensure exactly one Topup per month (income) - 20 months = 20 Topups
    # Plus 2000€ lump sum at beginning of each year
    dates = []
    
    # First, schedule exactly 20 monthly Topups (income) - always 1000€
    current_date = start_date
    topup_dates = []
    lump_sum_dates = []
    
    # Track years to add lump sum payments
    years_in_range = set()
    
    for month_num in range(20):
        # Topup around the 1st-5th of each month (when stipend arrives)
        topup_day = random.randint(1, 5)
        try:
            topup_date = datetime(current_date.year, current_date.month, topup_day)
            if topup_date <= end_date:
                topup_dates.append(topup_date)
                years_in_range.add(current_date.year)
        except ValueError:
            # If day doesn't exist (e.g., Feb 30), use 1st
            topup_date = datetime(current_date.year, current_date.month, 1)
            if topup_date <= end_date:
                topup_dates.append(topup_date)
                years_in_range.add(current_date.year)
        
        # Move to next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
    
    # Add 2000€ lump sum payments:
    # First lump sum: September 2024 (1st-5th)
    # Second lump sum: August 2025 (1st-5th)
    lump_sum_schedule = [
        datetime(2024, 9, random.randint(1, 5)),  # September 2024
        datetime(2025, 8, random.randint(1, 5))   # August 2025
    ]
    
    for lump_sum_date in lump_sum_schedule:
        if start_date <= lump_sum_date <= end_date:
            lump_sum_dates.append(lump_sum_date)
    
    # Generate remaining transaction dates (expenses and other transactions)
    # Target: ~35 transactions per month = ~700 total transactions
    remaining_transactions = num_transactions - len(topup_dates) - len(lump_sum_dates)
    for _ in range(remaining_transactions):
        days_offset = random.randint(0, date_range)
        date = start_date + timedelta(days=days_offset)
        # Weight towards weekdays (0-4 = Mon-Fri)
        if random.random() < 0.7:  # 70% chance of weekday
            weekday = random.randint(0, 4)
        else:
            weekday = random.randint(5, 6)
        # Adjust date to match desired weekday
        days_to_add = (weekday - date.weekday()) % 7
        date = date + timedelta(days=days_to_add)
        if date <= end_date:
            dates.append(date)
    
    # Combine and sort all dates, but remove duplicates from expense dates that match income dates
    # Create sets to check for conflicts
    topup_dates_set = set(topup_dates)
    lump_sum_dates_set = set(lump_sum_dates)
    income_dates_set = topup_dates_set | lump_sum_dates_set
    
    # Remove any expense dates that conflict with income dates
    dates = [d for d in dates if d not in income_dates_set]
    
    # Combine and sort all dates
    dates.extend(topup_dates)
    dates.extend(lump_sum_dates)
    dates.sort()
    
    # Generate transactions
    # Track which income dates have been processed
    topup_dates_used = set()
    lump_sum_dates_used = set()
    
    for i, date in enumerate(dates):
        # Check if this date is scheduled for a lump sum (2000€ at beginning of year)
        # Process each lump sum date exactly once
        if date in lump_sum_dates_set and date not in lump_sum_dates_used:
            transaction_type = 'Topup'  # Use Topup type for lump sum
            lump_sum_dates_used.add(date)
        # Check if this date is scheduled for a monthly Topup (1000€)
        # Process each monthly topup date exactly once
        elif date in topup_dates_set and date not in topup_dates_used:
            transaction_type = 'Topup'
            topup_dates_used.add(date)
        else:
            # Select transaction type based on probabilities (excluding Topup for non-scheduled dates)
            transaction_types_no_topup = {k: v for k, v in TRANSACTION_TYPES.items() if k != 'Topup'}
            total_prob = sum(transaction_types_no_topup.values())
            normalized_probs = {k: v/total_prob for k, v in transaction_types_no_topup.items()}
            transaction_type = np.random.choice(
                list(normalized_probs.keys()),
                p=list(normalized_probs.values())
            )
        
        # Select product
        if transaction_type in ['Interest', 'Exchange']:
            product = 'Deposit'
        elif transaction_type == 'Topup':
            product = random.choice(['Current', 'Savings'])
        else:
            product = random.choice(PRODUCTS)
        
        # Determine country and city based on date (before amount calculation to adjust for country)
        country, city = get_country_for_date(date, COUNTRY_TIMELINE)
        
        # Determine amount based on type and country
        # Cost of living adjustments for Erasmus student
        country_multiplier = {
            'Belgium': 1.2,  # Brussels is moderately expensive
            'Spain': 0.85,   # Barcelona is cheaper - good for students
            'Germany': 1.0,  # Berlin is moderate
            'France': 1.15   # Paris is expensive
        }.get(country, 1.0)
        
        if transaction_type == 'Card Payment':
            # Budget-conscious student spending amounts
            # Most transactions are small daily expenses (groceries, coffee, etc.)
            # Adjusted to target ~€2000 net savings (income - expenses ≈ 2000)
            # Balanced to account for rent of €618-625
            if random.random() < 0.75:  # 75% small transactions (groceries, coffee, etc.)
                base_amount = random.uniform(-30, -2)  # Daily groceries, coffee, small items
            elif random.random() < 0.92:  # 17% medium transactions (restaurant, shopping)
                base_amount = random.uniform(-72, -30)  # Restaurant meals, medium shopping
            else:  # 8% larger transactions (bigger shopping, events)
                base_amount = random.uniform(-145, -72)  # Larger purchases, events
            
            amount = round(base_amount * country_multiplier, 2)
            # Weight categories for realistic student lifestyle
            category_weights = {
                'Food & Dining': 0.45,      # Most common - groceries, restaurants (biggest expense after rent)
                'Transportation': 0.18,   # Public transport, travel between cities
                'Shopping & Retail': 0.12, # Clothes, essentials
                'Entertainment & Recreation': 0.08, # Movies, events, social activities
                'Utilities & Bills': 0.10, # Phone, internet (monthly bills)
                'Education': 0.04,        # Books, supplies
                'Personal Care & Services': 0.03  # Haircut, laundry
            }
            category = np.random.choice(list(category_weights.keys()), p=list(category_weights.values()))
        elif transaction_type == 'Transfer':
            # Transfers: rent (large negative, once per month), utilities, occasional positive
            if random.random() < 0.90:  # 90% negative (rent, bills)
                # Rent payment - once per month, around 380-450€ (adjusted to target ~€2000 savings)
                # Check if we're near the beginning of a month (rent is usually paid 1st-5th)
                if date.day <= 5 and random.random() < 0.25:  # 25% chance if early in month
                    amount = round(random.uniform(-625, -618), 2)  # Rent (around €618-625)
                else:
                    amount = round(random.uniform(-112, -10), 2)  # Other bills, utilities
            else:
                # Positive transfers (refunds, money from family, etc.)
                amount = round(random.uniform(1, 40), 2)
            category = 'Transfers & Payments'
        elif transaction_type == 'Topup':
            # Check if this is a lump sum (beginning of year) or monthly stipend
            if date in lump_sum_dates_set:
                # 2000€ lump sum at beginning of year
                amount = round(random.uniform(1995, 2005), 2)  # Around €2000
            else:
                # Monthly Erasmus stipend - exactly €1000 (never below)
                amount = round(random.uniform(1000, 1005), 2)  # €1000-1005, never below 1000
            category = 'Income & Deposits'
        elif transaction_type == 'Fee':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = 'Fees & Charges'
        elif transaction_type == 'Reward':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = 'Income & Deposits'
        elif transaction_type == 'Interest':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = 'Financial Services'
        elif transaction_type == 'Card Refund':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = random.choice(['Food & Dining', 'Shopping & Retail', 'Transportation'])
        else:  # Exchange
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = 'Other'
        
        # Determine country and city based on date
        country, city = get_country_for_date(date, COUNTRY_TIMELINE)
        
        # Select merchant/description based on country
        country_merchants = COUNTRY_MERCHANTS.get(country, {})
        if category in country_merchants:
            merchants = country_merchants[category]
        else:
            merchants = MERCHANTS_BY_CATEGORY.get(category, ['Merchant'])
        merchant = random.choice(merchants)
        
        # Generate hour based on weights (normalize to sum to 1)
        hours = list(HOUR_WEIGHTS.keys())
        weights = list(HOUR_WEIGHTS.values())
        weights_sum = sum(weights)
        weights_normalized = [w / weights_sum for w in weights]
        hour = np.random.choice(hours, p=weights_normalized)
        
        # Calculate weekday name
        weekday_name = date.strftime('%A')
        
        # Update balance
        current_balance += amount
        
        # Calculate absolute amount
        amount_abs = abs(amount)
        
        # Create transaction record
        transaction = {
            'Type': transaction_type,
            'Product': product,
            'Amount': amount,
            'Balance': round(current_balance, 2),
            'Year': date.year,
            'Month': date.month,
            'Day': date.day,
            'Weekday': weekday_name,
            'Hour': hour,
            'Amount_Abs': amount_abs,
            'Description_Anon': merchant,
            'Merchant_Category': category,
            'Country': country,
            'City': city
        }
        
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def main():
    """Generate and save dummy data."""
    print("Generating dummy transaction data...")
    print(f"Transactions: {NUM_TRANSACTIONS}")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    
    df = generate_transactions(NUM_TRANSACTIONS, START_DATE, END_DATE)
    
    # Save to CSV
    output_file = 'Dataset - Dummy Data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Dummy data generated successfully!")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Total transactions: {len(df)}")
    print(f"💰 Final balance: €{df['Balance'].iloc[-1]:,.2f}")
    print(f"📈 Total income: €{df[df['Amount'] > 0]['Amount'].sum():,.2f}")
    print(f"📉 Total expenses: €{abs(df[df['Amount'] < 0]['Amount'].sum()):,.2f}")
    print(f"\n💡 To use dummy data, rename it to 'Dataset - Sara Saad.csv' or update dashboard.py")

if __name__ == "__main__":
    main()

