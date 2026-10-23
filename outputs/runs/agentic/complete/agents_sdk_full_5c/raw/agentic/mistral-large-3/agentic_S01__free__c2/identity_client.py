import os
from typing import Optional
from firebase_admin import auth, initialize_app


def get_firebase_auth_client() -> auth.Client:
    """Initialize and return Firebase Auth client."""
    if not auth._apps:
        initialize_app(options={
            "projectId": os.getenv("FIREBASE_PROJECT_ID")
        })
    return auth


def load_firebase_config() -> dict:
    """Load Firebase configuration from environment variables."""
    return {
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "api_key": os.getenv("FIREBASE_API_KEY")
    }