import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
from scipy.spatial import KDTree

class FundraisingDataGenerator:
    def __init__(self, config):
        """Initialize generator with configuration"""
        self.config = config
        self.contact_manager = ContactManager(config.get('CHANNELS', {}))
        self.faker = Faker(config.get('LOCALISATION', 'fr_FR'))
        
    def generate_data(self):
        """Generate fundraising data based on configuration"""
        transactions = []
        current_year = self.config.get('FIRST_YEAR', 2014)
        years = self.config.get('YEARS', 10)
        
        for year in range(years):
            year_transactions = self._generate_year_data(current_year + year)
            transactions.extend(year_transactions)
            
        # Convert to DataFrame
        transactions_df = pd.DataFrame(transactions)
        
        # Generate contacts based on transactions
        contacts_df = self._generate_contacts(transactions_df)
        
        return transactions_df, contacts_df
    
    def _generate_year_data(self, year):
        """Generate transactions for a specific year"""
        year_transactions = []
        
        for channel_name, channel_data in self.config['CHANNELS'].items():
            channel_transactions = self._generate_channel_data(
                year, 
                channel_name, 
                channel_data
            )
            year_transactions.extend(channel_transactions)
            
        return year_transactions
    
    def _generate_channel_data(self, year, channel_name, channel_data):
        """Generate transactions for a specific channel"""
        channel_transactions = []
        
        for campaign_type, campaign_info in channel_data['campaigns'].items():
            campaign_transactions = self._generate_campaign_data(
                year,
                channel_name,
                campaign_type,
                campaign_info,
                channel_data
            )
            channel_transactions.extend(campaign_transactions)
            
        return channel_transactions

    def _generate_campaign_data(self, year, channel, campaign_type, campaign_info, channel_data):
        """Generate transactions for a specific campaign"""
        transactions = []
        num_campaigns = campaign_info.get('nb', 1)
        
        for _ in range(num_campaigns):
            # Generate campaign metadata
            campaign_meta = self._generate_campaign_metadata(year, channel, campaign_type)
            
            # Get contacts and generate transactions
            nb_reach, nb_sent, contact_ids = self.contact_manager.get_or_create_contacts(
                campaign_type, 
                channel, 
                random.uniform(0.85, 1.15)
            )
            
            if nb_sent and contact_ids:
                campaign_transactions = self._create_campaign_transactions(
                    campaign_meta,
                    nb_reach,
                    nb_sent,
                    contact_ids,
                    campaign_info,
                    channel_data
                )
                transactions.extend(campaign_transactions)
        
        return transactions

class ContactManager:
    """Manage contact generation and assignment"""
    def __init__(self, channels):
        self.existing_contacts = {channel: [] for channel in channels}
        self.channels = channels

    def get_or_create_contacts(self, campaign_type, channel, randomness=1.0):
        """Get existing contacts or create new ones based on campaign type"""
        channel_info = self.channels[channel]
        
        if campaign_type == 'prospecting':
            return self._handle_prospecting(channel, channel_info, randomness)
        elif campaign_type == 'retention':
            return self._handle_retention(channel, channel_info, randomness)
        
        return 0, 0, []

    def _handle_prospecting(self, channel, channel_info, randomness):
        """Handle prospecting campaign contact generation"""
        num_required = channel_info["campaigns"]["prospecting"]["max_reach_contact"]
        transformation_rate = (
            channel_info["campaigns"]["prospecting"]["transformation_rate"] 
            * randomness
        )
        
        # Generate new contacts
        new_contacts = self._generate_contact_ids(int(num_required * transformation_rate))
        self.existing_contacts[channel].extend(new_contacts)
        
        return num_required, len(new_contacts), new_contacts

    def _handle_retention(self, channel, channel_info, randomness):
        """Handle retention campaign contact selection"""
        # Get cross-sell contacts if configured
        cross_sell_info = channel_info["campaigns"]["retention"].get("cross_sell", [])
        contacts = self._get_cross_sell_contacts(channel, cross_sell_info)
        
        nb_reach = len(contacts)
        transformation_rate = (
            channel_info["campaigns"]["retention"]["transformation_rate"] 
            * randomness
        )
        nb_sent = int(nb_reach * transformation_rate)
        
        return nb_reach, nb_sent, contacts[:nb_sent]

    def _generate_contact_ids(self, count):
        """Generate unique contact IDs"""
        return [
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            for _ in range(count)
        ]
