import os
from urllib.parse import urlencode

class IdentityClientConfig:
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")
    AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{{AUTH0_DOMAIN}}/api/v2/")

    GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
    AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID") # For Google Cloud Translation and Firestore
