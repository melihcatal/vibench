import firebase_admin
from firebase_admin import credentials
from dataclasses import dataclass

@dataclass
class FirebaseConfig:
    project_id: str
    # In a real application, you might load service account credentials here
    # For simplicity, we'll assume the project ID is sufficient for initialization
    # if running in a Google Cloud environment or with FIREBASE_CONFIG environment variable set.

def get_firebase_app(config: FirebaseConfig):
    try:
        return firebase_admin.get_app()
    except ValueError:
        # If running outside a Google Cloud environment, you might need
        # to explicitly provide credentials. For this exercise, we assume
        # that if the app is not found, we can initialize it with just the project_id.
        # A more robust solution would involve loading service account credentials.
        # For local development, 'firebase_admin.initialize_app()' can often infer
        # credentials if GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        return firebase_admin.initialize_app(options={"projectId": config.project_id})
