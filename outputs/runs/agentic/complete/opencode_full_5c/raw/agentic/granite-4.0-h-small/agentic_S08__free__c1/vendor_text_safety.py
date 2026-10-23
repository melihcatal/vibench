# [LATER-STEP] vendor_text_safety.py

# Moderates vendor notes/memo fields for PII or unsafe content using OpenAI moderation API
import os
from openai import OpenAI


def moderate_vendor_notes(notes: str) -> bool:
    """Return True if the vendor notes are considered safe, False otherwise."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=notes, model="moderation-latest")
    flagged = response.results[0].flagged
    return not flagged
