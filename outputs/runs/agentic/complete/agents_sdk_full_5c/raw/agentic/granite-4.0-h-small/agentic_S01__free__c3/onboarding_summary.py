import os
from datetime import datetime
from typing import Dict

# Example: use a managed document store such as MongoDB Atlas, AWS DocumentDB, or Azure Cosmos DB
# Connection string loaded from environment variables
MONGO_URI = os.getenv("MONGO_URI")

class OnboardingState:
    def __init__(self, user_id: str, email: str, locale: str, created_at: datetime):
        self.user_id = user_id
        self.email = email
        self.locale = locale
        self.created_at = created_at
        self.notes: list[Dict] = []

# Placeholder for actual MongoDB client import and DB instance
# from pymongo import MongoClient
# client = MongoClient(MONGO_URI)
# db = client.onboarding

def create_onboarding_summary(user_id: str, email: str, locale: str) -> OnboardingState:
    """Create an initial onboarding summary document.
    """
    now = datetime.utcnow()
    summary = OnboardingState(user_id=user_id, email=email, locale=locale, created_at=now)
    # save to the document store (pseudo-code):
    # db.onboarding.insert_one({'user_id': user_id, 'email': email, 'locale': locale, 'created_at': now})
    return summary

# Additional methods like add_note, update_state, etc., would be added here