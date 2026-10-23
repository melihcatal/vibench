from typing import TypedDict, Any
import re

def normalize_email(email: str) -> str:
    return re.sub(r'\s+', '', email.lower())

def build_signup_payload(email: str, password: str) -> dict:
    return {
        "email": normalize_email(email),
        "password": password
    }

def build_login_payload(email: str, password: str) -> dict:
    return build_signup_payload(email, password)

def build_refresh_payload(refresh_token: str) -> dict:
    return {"refresh_token": refresh_token}