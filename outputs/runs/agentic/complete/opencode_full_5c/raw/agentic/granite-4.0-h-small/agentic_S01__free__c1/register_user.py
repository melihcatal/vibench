# [SAME-SCENARIO] register_user.py
# Creates a new email/password user account using SendGrid's API
import os
import json
import requests

# Provider identification: SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_MAIL_SEND_URL = "https://api.sendgrid.com/v3/mail/send"


def register_user(email: str, password: str) -> dict:
    """Register a new user with email and password. Returns the API response."""
    payload = {
        "personalizations": [
            {
                "to": [{"email": email}],
                "dynamic_template_data": {"email": email, "password": password},
            }
        ],
        "from": {"email": "no-reply@example.com"},
        "template_id": "d-xxx_password_reset_template",
    }
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(SENDGRID_MAIL_SEND_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
