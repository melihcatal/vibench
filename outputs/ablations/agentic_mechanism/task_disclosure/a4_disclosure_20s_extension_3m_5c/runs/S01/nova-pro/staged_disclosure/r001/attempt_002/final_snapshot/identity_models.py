from typing import Dict, Any

def create_account_request(email: str, password: str) -> Dict[str, Any]:
    return {
        'email': email,
        'password': password
    }

def account_creation_response(success: bool, message: str) -> Dict[str, Any]:
    return {
        'success': success,
        'message': message
    }

def normalize_email(email: str) -> str:
    return email.lower().strip()