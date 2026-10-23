import os
import json
from typing import Dict, Any

# Provider – using OpenAI Moderation for vendor notes moderation
OPENAI_MODERATION_ENDPOINT = os.getenv("OPENAI_MODERATION_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def moderate_vendor_note(note: str) -> bool:
    """Return True if the vendor note content is safe, False otherwise.","""
    # Placeholder for HTTP request to OpenAI Moderation endpoint
    # response = requests.post(OPENAI_MODERATION_ENDPOINT, json={"input": note}, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})
    # result = response.json()
    # For demo purposes we simply allow all notes (no harmful content)
    return True
