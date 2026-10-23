import os
import requests
from document_models import Expense

def moderate_vendor_text(expense: Expense, moderation_endpoint: str, api_key: str) -> str:
    """Calls a content moderation service for any vendor notes or memo fields."""
    vendor_note = expense.metadata.get("vendor_note", "")
    if not vendor_note:
        return vendor_note  # Nothing to moderate
    payload = {
        "text": vendor_note,
        "categories": ["hate", "harassment", "self_harm", "sexual", "violent"]
    }
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(moderation_endpoint, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Moderation API error: {response.status_code}")
    result = response.json()
    # Simple safety check: if any flag is true, replace note with placeholder
    if result.get("flagged", False):
        return "[REDACTED: VENDOR NOTE FLAGGED]"
    return vendor_note
