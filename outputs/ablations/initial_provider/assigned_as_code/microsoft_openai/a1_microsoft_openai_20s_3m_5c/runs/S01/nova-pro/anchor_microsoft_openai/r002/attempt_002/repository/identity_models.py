from typing import Dict


def normalize_payload(payload: Dict):
    return {
        'email': payload['email'],
        'password': payload['password']
    }


def parse_response(response):
    return response.json()
