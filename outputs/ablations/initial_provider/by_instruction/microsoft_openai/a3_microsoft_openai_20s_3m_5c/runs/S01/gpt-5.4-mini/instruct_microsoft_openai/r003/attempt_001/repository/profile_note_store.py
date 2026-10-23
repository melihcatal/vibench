import os

import requests


AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")
AIRTABLE_TABLE = os.environ.get("AIRTABLE_TABLE", "OnboardingNotes")


def profile_note_store(record: dict) -> dict:
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"
    headers = {"Authorization": f"Bearer {os.environ.get('AIRTABLE_API_KEY', '')}", "Content-Type": "application/json"}
    response = requests.post(url, json={"fields": record}, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
