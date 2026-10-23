import re
from typing import Dict, Any

def normalize_email(email: str) -> str:
    return re.sub(r'\s+', '', email.lower().strip())

def build_signup_payload(email: str, password: str) -> Dict[str, Any]:
    return {"email": normalize_email(email), "password": password}

def extract_tokens(session: Any) -> Dict[str, str]:
    return {
        "access_token": getattr(session, 'access_token', ''),
        "refresh_token": getattr(session, 'refresh_token', ''),
    }