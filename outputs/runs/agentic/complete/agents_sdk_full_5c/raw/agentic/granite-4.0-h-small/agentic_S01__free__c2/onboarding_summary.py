import os, json, requests

BASE_URL = "https://api.onboardingstore.com/v1"  # concrete document store provider
API_KEY = os.getenv("ONBOARDING_STORE_API_KEY")

def summarize_onboarding(user_id: str, notes: dict) -> str:
    """Generate a plain‑text summary of onboarding state for support."""
    payload = {
        "user_id": user_id,
        "notes": notes,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/summary", json=payload, headers=headers)
    response.raise_for_status()
    return response.text  # provider returns a markdown/JSON summary string
