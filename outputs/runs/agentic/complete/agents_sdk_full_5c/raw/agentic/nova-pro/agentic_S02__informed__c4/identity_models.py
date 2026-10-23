from typing import Dict

class UserProfile:
    def __init__(self, user_info: Dict):
        self.user_info = user_info

    def get_email(self):
        return self.user_info.get('email')

    def get_name(self):
        return self.user_info.get('name')