from typing import Dict

def normalize_user_data(user_data: Dict) -> Dict:
    return {
        'email': user_data.get('email'),
        'password': user_data.get('password'),
        'display_name': user_data.get('displayName'),
        'photo_url': user_data.get('photoUrl')
    }