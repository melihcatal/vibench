from typing import Dict

def normalize_user_payload(payload: Dict) -> Dict:
    return {
        'email': payload['email'],
        'password': payload['password']
    }