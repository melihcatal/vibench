import os
from document_models import NormalizedExpense
import requests

# Watsonx.ai guardrails (text safety) - using REST API
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
CONTENT_SAFETY_ENDPOINT = os.getenv("WATSONX_GUARDRAILS_ENDPOINT")


def moderate_vendor_notes(vendor_notes: str) -> bool:
    payload = {"text": vendor_notes}
    headers = {
        "Authorization": f"Bearer {WATSONX_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{CONTENT_SAFETY_ENDPOINT}/moderation", json=payload, headers=headers
    )
    if response.status_code == 200:
        result = response.json()
        # Assuming result['pass'] indicates safe content
        return result.get("pass", False)
    raise Exception(f"Guardrails check failed: {response.text}")
