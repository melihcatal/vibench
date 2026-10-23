import os

def get_auth0_config():
    return {
        "AUTH0_DOMAIN": os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com"),
        "AUTH0_CLIENT_ID": os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID"),
        "AUTH0_CLIENT_SECRET": os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET"),
        "AUTH0_REDIRECT_URI": os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/callback"),
    }

def get_google_oidc_config():
    return {
        "GOOGLE_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"),
        "GOOGLE_REDIRECT_URI": os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/google_callback"),
        "GOOGLE_DISCOVERY_URL": "https://accounts.google.com/.well-known/openid-configuration",
    }

def get_gemini_config():
    return {
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY"),
        "GEMINI_MODEL_ID": os.environ.get("GEMINI_MODEL_ID", "gemini-pro"),
    }

def get_perspective_api_config():
    return {
        "PERSPECTIVE_API_KEY": os.environ.get("PERSPECTIVE_API_KEY", "YOUR_PERSPECTIVE_API_KEY"),
        "PERSPECTIVE_API_ENDPOINT": "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    }

def get_google_translation_config():
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    return {
        "GOOGLE_PROJECT_ID": os.environ.get("GOOGLE_PROJECT_ID", "your-gcp-project-id"),
    }

def get_firestore_config():
    # Google Cloud Firestore uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    return {
        "GOOGLE_PROJECT_ID": os.environ.get("GOOGLE_PROJECT_ID", "your-gcp-project-id"),
        "FIRESTORE_COLLECTION_NAME": os.environ.get("FIRESTORE_COLLECTION_NAME", "login_audit_records"),
    }
