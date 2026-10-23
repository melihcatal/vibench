# [LATER-STEP] profile_note_store.py
# Persist onboarding notes and support metadata in a managed document store

# Example using MongoDB Atlas Data API (concrete provider)

import os

ATLAS_API_KEY = os.getenv("ATLAS_API_KEY")  # <-- set your Atlas Data API key
ATLAS_CLUSTER_URL = os.getenv(
    "ATLAS_CLUSTER_URL"
)  # <-- full URL e.g., https://cluster0.mongodb.net
ATLAS_DATABASE = os.getenv("ATLAS_DATABASE", "email_password_db")
ATLAS_COLLECTION = os.getenv("ATLAS_COLLECTION", "onboarding_notes")

BASE_URL = f"{ATLAS_CLUSTER_URL}/api/data/v1"

import requests
import json

HEADERS = {"Content-Type": "application/json", "api-key": ATLAS_API_KEY}


def store_note(user_id: str, note: str, metadata: dict = None) -> dict:
    """Insert a note for a given user into the onboarding_notes collection.
    Returns the API response JSON.
    """
    if not (ATLAS_API_KEY and ATLAS_CLUSTER_URL):
        raise RuntimeError("Atlas Data API environment variables not configured")
    payload = {
        "fullDocument": {
            "userId": user_id,
            "note": note,
            "metadata": metadata or {},
            "createdAt": datetime.utcnow().isoformat() + "Z",
        }
    }
    endpoint = f"{BASE_URL}/insertOne/{ATLAS_DATABASE}/{ATLAS_COLLECTION}"
    response = requests.post(endpoint, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# Example usage:
# result = store_note("user123", "User prefers dark mode.", {"locale": "es"})
