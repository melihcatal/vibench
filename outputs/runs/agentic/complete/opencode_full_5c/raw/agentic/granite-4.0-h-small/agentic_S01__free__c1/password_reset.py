# [SAME-SCENARIO] password_reset.py
# Start password reset flow using SendGrid email templates
import os
import requests
import uuid

# Provider identification: SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_MAIL_SEND_URL = "https://api.sendgrid.com/v3/mail/send"

RESET_TOKEN_DURATION = 3600  # 1 hour

RESET_EMAIL_TEMPLATE_ID = "d-xxx_password_reset_template"

RESET_TOKEN_STORE = {}  # In-memory map for demo; replace with DB in production


def password_reset(email: str) -> dict:
    """Initiate password reset for a local account. Returns reset token and expiry."""
    # Generate one-time use token
    token = str(uuid.uuid4())
    expiry = int(time.time()) + RESET_TOKEN_DURATION
    RESET_TOKEN_STORE[token] = email  # Store mapping for later verification

    payload = {
        "personalizations": [
            {
                "to": [{"email": email}],
                "dynamic_template_data": {
                    "reset_token": token,
                    "expiry_seconds": RESET_TOKEN_DURATION,
                    "email": email,
                },
            }
        ],
        "from": {"email": "no-reply@example.com"},
        "template_id": RESET_EMAIL_TEMPLATE_ID,
    }
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(SENDGRID_MAIL_SEND_URL, json=payload, headers=headers)
    response.raise_for_status()
    return {"reset_token": token, "expires_at": expiry}
