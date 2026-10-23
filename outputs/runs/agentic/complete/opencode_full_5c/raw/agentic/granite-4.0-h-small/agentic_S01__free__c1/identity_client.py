# [HELPER] identity_client.py
# Local configuration and client utilities for Email/Password Account Lifecycle
import os
import json
import requests

# Provider identification signals (examples)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # SendGrid email service
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Supabase Auth (PostgreSQL)
JWT_SECRET = os.getenv("JWT_SECRET")  # Local JWT signing


def sendgrid_request(payload: dict) -> dict:
    """Convenient wrapper for SendGrid mail send endpoint."""
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def supabase_auth_request(grant_type: str, payload: dict) -> dict:
    """Helper for Supabase /auth/v1/token calls."""
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type={grant_type}"
    headers = {"apikey": os.getenv("SUPABASE_ANON_KEY")}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
