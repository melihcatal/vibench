import os

# Okta Configuration
OKTA_ORG_URL = os.environ.get("OKTA_ORG_URL", "https://{your-okta-domain}.okta.com")
OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID", "{your-okta-client-id}")
OKTA_CLIENT_SECRET = os.environ.get("OKTA_CLIENT_SECRET", "{your-okta-client-secret}")
OKTA_REDIRECT_URI = os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8000/callback")

# MongoDB Atlas Configuration
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://user:password@cluster.mongodb.net/admin")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "federated_login_audits")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "audit_records")

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Google Cloud Translation Configuration (usually handled by GOOGLE_APPLICATION_CREDENTIALS)
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
