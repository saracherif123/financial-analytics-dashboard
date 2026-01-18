"""
Generate dummy financial transaction data similar to the original dataset structure.
This creates realistic but fake data for public deployment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
NUM_TRANSACTIONS = 900  # Similar to original dataset
START_DATE = datetime(2024, 9, 1)
END_DATE = datetime(2025, 12, 31)  # Extended to include France period

# Country timeline (based on user's travel)
# Timeline: 6 months Belgium, 6 months Spain, 2 months Germany, rest in Paris France
COUNTRY_TIMELINE = [
    {'country': 'Belgium', 'city': 'Brussels', 'start': datetime(2024, 9, 1), 'end': datetime(2025, 3, 1)},  # 6 months
    {'country': 'Spain', 'city': 'Barcelona', 'start': datetime(2025, 3, 1), 'end': datetime(2025, 9, 1)},  # 6 months
    {'country': 'Germany', 'city': 'Nuremberg', 'start': datetime(2025, 9, 1), 'end': datetime(2025, 11, 1)},  # 2 months
    {'country': 'France', 'city': 'Paris', 'start': datetime(2025, 11, 1), 'end': datetime(2026, 1, 1)},  # Rest (will be adjusted to END_DATE in function)
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
        'Food & Dining': ['REWE', 'EDEKA', 'Aldi', 'Lidl', 'Bakery Munich', 'Beer Garden'],
        'Transportation': ['Deutsche Bahn', 'MVG Munich', 'Bolt Munich'],
        'Shopping & Retail': ['H&M Munich', 'Müller', 'DM Drogerie'],
        'Other': ['Oktoberfest Shop', 'BMW Museum', 'Munich Souvenirs']
    },
    'France': {
        'Food & Dining': ['Carrefour Paris', 'Monoprix', 'Franprix', 'Boulangerie', 'Café Parisien'],
        'Transportation': ['RATP', 'SNCF', 'Bolt Paris', 'Vélib'],
        'Shopping & Retail': ['Galeries Lafayette', 'Printemps', 'FNAC'],
        'Other': ['Louvre Shop', 'Eiffel Tower', 'Paris Souvenirs']
    }
}

# Transaction types and their probabilities
TRANSACTION_TYPES = {
    'Card Payment': 0.45,
    'Transfer': 0.30,
    'Topup': 0.15,
    'Fee': 0.03,
    'Reward': 0.02,
    'Interest': 0.03,
    'Card Refund': 0.01,
    'Exchange': 0.01
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
AMOUNT_RANGES = {
    'Card Payment': (-200, -1),
    'Transfer': (-2000, 2000),
    'Topup': (100, 5000),
    'Fee': (-50, -1),
    'Reward': (5, 50),
    'Interest': (0.1, 5),
    'Card Refund': (1, 200),
    'Exchange': (-1000, 1000)
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
    # Update last country's end date to END_DATE
    country_timeline[-1]['end'] = datetime(2025, 10, 1)
    
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
    
    # Initial balance
    current_balance = 1000.0
    
    # Generate dates with some clustering (more transactions on weekdays)
    dates = []
    for _ in range(num_transactions):
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
    
    dates.sort()
    
    # Generate transactions
    for i, date in enumerate(dates):
        # Select transaction type based on probabilities
        transaction_type = np.random.choice(
            list(TRANSACTION_TYPES.keys()),
            p=list(TRANSACTION_TYPES.values())
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
        
        # Determine amount based on type and country (Belgium should be most expensive)
        country_multiplier = {
            'Belgium': 1.5,  # 50% more expensive - MOST EXPENSIVE
            'Spain': 1.0,    # Baseline
            'Germany': 0.9,  # 10% less expensive
            'France': 1.1    # 10% more expensive
        }.get(country, 1.0)
        
        if transaction_type == 'Card Payment':
            base_amount = random.uniform(*AMOUNT_RANGES[transaction_type])
            amount = round(base_amount * country_multiplier, 2)
            category = random.choice(['Food & Dining', 'Transportation', 'Shopping & Retail', 
                                    'Entertainment & Recreation', 'Utilities & Bills', 'Other'])
        elif transaction_type == 'Transfer':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
            category = 'Transfers & Payments'
        elif transaction_type == 'Topup':
            amount = round(random.uniform(*AMOUNT_RANGES[transaction_type]), 2)
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

