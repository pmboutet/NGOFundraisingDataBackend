import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
from .contact_manager import ContactManager

class FundraisingDataGenerator:
    def __init__(self, config):
        self.config = config
        self.contact_manager = ContactManager(config.get('CHANNELS', {}))
        self.faker = Faker(config.get('LOCALISATION', 'fr_FR'))
        
    def generate(self):
        """Main method to generate fundraising data"""
        transactions = []
        current_year = self.config.get('FIRST_YEAR', 2014)
        years = self.config.get('YEARS', 10)
        
        # Generate transactions for each year
        for year in range(years):
            year_data = self._generate_year_data(current_year + year)
            transactions.extend(year_data)
        
        # Convert to DataFrame
        transactions_df = pd.DataFrame(transactions)
        
        # Generate contacts based on transactions
        contacts_df = self._generate_contacts(transactions_df)
        
        return transactions_df, contacts_df
    
    def _generate_year_data(self, year):
        transactions = []
        
        for channel_name, channel_info in self.config['CHANNELS'].items():
            for campaign_type, campaign_config in channel_info.get('campaigns', {}).items():
                num_campaigns = campaign_config.get('nb', 1)
                
                for _ in range(num_campaigns):
                    campaign_data = self._generate_campaign(year, channel_name, channel_info, campaign_type, campaign_config)
                    transactions.extend(campaign_data)
        
        return transactions
    
    def _generate_campaign(self, year, channel, channel_info, campaign_type, campaign_config):
        # Generate campaign dates
        start_day = random.randint(1, 365)
        start_date = datetime(year, 1, 1) + timedelta(days=start_day)
        end_date = start_date + timedelta(days=channel_info.get('duration', 30))
        
        # Get contacts
        randomness = random.uniform(0.85, 1.15)
        nb_reach, nb_sent, contacts = self.contact_manager.get_or_create_contacts(
            campaign_type, channel, randomness
        )
        
        if not contacts:
            return []
            
        # Generate transactions
        transactions = []
        avg_donation = campaign_config.get('avg_donation', 50)
        std_deviation = campaign_config.get('std_deviation', 10)
        
        for contact_id in contacts:
            transaction = {
                'date': self._generate_transaction_date(start_date, end_date),
                'campaign_start': start_date,
                'campaign_end': end_date,
                'channel': channel,
                'campaign_name': f"{year}-{start_day:03d}_{channel}_{campaign_type}",
                'campaign_type': campaign_type,
                'donation_amount': max(1, random.gauss(avg_donation, std_deviation)),
                'payment_method': self._select_payment_method(channel_info),
                'cost': channel_info.get('cost_per_reach', 1),
                'reactivity': nb_reach / max(1, nb_sent),
                'contact_id': contact_id
            }
            transactions.append(transaction)
        
        return transactions
    
    def _generate_transaction_date(self, start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)
    
    def _select_payment_method(self, channel_info):
        payment_methods = channel_info.get('payment', {'card': 1.0})
        methods, weights = zip(*payment_methods.items())
        return random.choices(methods, weights=weights)[0]
    
    def _generate_contacts(self, transactions_df):
        # Group by contact_id to get unique contacts
        unique_contacts = transactions_df.groupby('contact_id').agg({
            'donation_amount': ['mean', 'count'],
            'date': 'min'
        }).reset_index()
        
        contacts_data = []
        
        for _, row in unique_contacts.iterrows():
            contact = {
                'contact_id': row['contact_id'],
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'email': self.faker.email(),
                'phone': self.faker.phone_number(),
                'address': self.faker.address(),
                'creation_date': row['date']['min'],
                'avg_donation': row['donation_amount']['mean'],
                'total_transactions': row['donation_amount']['count']
            }
            contacts_data.append(contact)
        
        return pd.DataFrame(contacts_data)