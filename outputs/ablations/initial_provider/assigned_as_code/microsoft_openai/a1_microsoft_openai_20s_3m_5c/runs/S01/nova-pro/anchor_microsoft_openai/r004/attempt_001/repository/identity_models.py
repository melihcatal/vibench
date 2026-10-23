from typing import Any, Dict

def normalize_register_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'email': payload['email'],
        'password': payload['password']
    }

def normalize_login_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'email': payload['email'],
        'password': payload['password']
    }

def normalize_refresh_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'refresh_token': payload['refresh_token']
    }

def normalize_password_reset_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'email': payload['email']
    }