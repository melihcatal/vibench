from typing import Dict


def normalize_register_payload(payload: Dict) -> Dict:
    return {
        "email": payload["email"],
        "password": payload["password"]
    }


def normalize_login_payload(payload: Dict) -> Dict:
    return {
        "email": payload["email"],
        "password": payload["password"]
    }


def normalize_refresh_payload(payload: Dict) -> Dict:
    return {
        "refresh_token": payload["refresh_token"]
    }


def normalize_password_reset_payload(payload: Dict) -> Dict:
    return {
        "email": payload["email"]
    }
