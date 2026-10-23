from typing import Dict, Any

def normalize_email_password_request(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'email': request.get('email'),
        'password': request.get('password')
    }

def normalize_email_password_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'status': response.get('status'),
        'message': response.get('message'),
        'tokens': response.get('tokens')
    }

def create_email_password_request(email: str, password: str) -> Dict[str, Any]:
    return {
        'email': email,
        'password': password
    }

def extract_tokens_from_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response.get('tokens', {})