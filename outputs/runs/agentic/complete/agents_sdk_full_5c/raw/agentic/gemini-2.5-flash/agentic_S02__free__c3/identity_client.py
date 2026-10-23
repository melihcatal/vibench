import os

# Auth0 Configuration (replace with your actual values)
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-your-domain.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")

# Google Cloud Configuration (replace with your actual values)
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
