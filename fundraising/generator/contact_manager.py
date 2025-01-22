import random
import string

class ContactManager:
    def __init__(self, channels):
        self.existing_contacts = {channel: [] for channel in channels}
        self.channels = channels

    def get_or_create_contacts(self, campaign_type, channel, randomness=1.0):
        channel_info = self.channels.get(channel, {})
        
        if campaign_type == 'prospecting':
            return self._handle_prospecting(channel, channel_info, randomness)
        elif campaign_type == 'retention':
            return self._handle_retention(channel, channel_info, randomness)
        
        return 0, 0, []
    
    def _generate_contact_ids(self, count):
        return [
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            for _ in range(count)
        ]
    
    def _handle_prospecting(self, channel, channel_info, randomness):
        campaign_info = channel_info.get('campaigns', {}).get('prospecting', {})
        max_reach = campaign_info.get('max_reach_contact', 1000)
        transformation_rate = campaign_info.get('transformation_rate', 0.1) * randomness
        
        num_contacts = int(max_reach * transformation_rate)
        new_contacts = self._generate_contact_ids(num_contacts)
        self.existing_contacts[channel].extend(new_contacts)
        
        return max_reach, len(new_contacts), new_contacts

    def _handle_retention(self, channel, channel_info, randomness):
        campaign_info = channel_info.get('campaigns', {}).get('retention', {})
        existing_contacts = self.existing_contacts.get(channel, [])
        
        if not existing_contacts:
            return 0, 0, []
            
        transformation_rate = campaign_info.get('transformation_rate', 0.2) * randomness
        num_contacts = int(len(existing_contacts) * transformation_rate)
        
        return len(existing_contacts), num_contacts, random.sample(existing_contacts, min(num_contacts, len(existing_contacts)))