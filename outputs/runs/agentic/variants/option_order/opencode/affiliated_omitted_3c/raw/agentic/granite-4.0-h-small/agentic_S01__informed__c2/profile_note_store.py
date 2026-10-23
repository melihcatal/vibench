# profile_note_store.py
# Persist onboarding notes and support metadata in a managed document store (MongoDB Atlas reference)

import os
import json
from typing import Dict, Any
from pymongo import MongoClient
from identity_models import normalize_user_profile, RegisterUserRequest

# MongoDB Atlas connection string (set as environment variable)
MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
if not MONGODB_ATLAS_URI:
    raise RuntimeError("Set MONGODB_ATLAS_URI environment variable")

client = MongoClient(MONGODB_ATLAS_URI)
# Choose a database and collection (you may adjust names as needed)
db = client["email_password_onboarding"]
collection = db["users"]


def store_notes(payload: RegisterUserRequest, user_id: str) -> None:
    """Save onboarding notes and normalized profile to MongoDB."""
    payload_dict = {
        "user_id": user_id,
        "email": payload.email,
        "notes": payload.notes,
        "created_at": json.dumps({"$date": int(os.time() * 1000)}),  # ISODate
    }
    # Normalized profile can be fetched from elsewhere; here we just store the minimal fields.
    profile = {
        "email": payload.email,
        "locale": "en-US",
        "status": "pending",
    }
    document = {**profile, **payload_dict}
    collection.replace_one({"user_id": user_id}, document, upsert=True)


# Example usage (do not run in production script)
if __name__ == "__main__":
    user = RegisterUserRequest(
        email="dave@example.com",
        password="SecureP@ss123!",
        notes="Wants to enable 2FA after completing tutorial.",
    )
    # Simulate a user_id generation step (e.g., DB insert returning id)
    fake_user_id = "user-456"
    store_notes(user, fake_user_id)
    print(f"Stored onboarding notes for user {fake_user_id}")
