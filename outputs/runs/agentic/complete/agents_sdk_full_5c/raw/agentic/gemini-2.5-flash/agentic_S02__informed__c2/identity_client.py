import os

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

# Google Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")

# Azure AI Content Safety Configuration
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "YOUR_AZURE_CONTENT_SAFETY_KEY")

# Google Cloud Translation Configuration
# GOOGLE_APPLICATION_CREDENTIALS should be set in environment for SDK to pick up.
# For programmatic setup, you'd load credentials explicitly.

# Google Firestore Configuration
# GOOGLE_APPLICATION_CREDENTIALS should be set in environment for SDK to pick up.
FIRESTORE_PROJECT_ID = os.getenv("FIRESTORE_PROJECT_ID", "YOUR_FIRESTORE_PROJECT_ID")
FIRESTORE_COLLECTION_AUDIT = os.getenv("FIRESTORE_COLLECTION_AUDIT", "login_audit_records")
