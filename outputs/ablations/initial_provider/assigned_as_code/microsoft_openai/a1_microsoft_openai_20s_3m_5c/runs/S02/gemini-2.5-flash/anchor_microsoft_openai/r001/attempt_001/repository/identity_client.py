import os
from typing import Dict, Any, Optional

def get_auth0_config() -> Dict[str, str]:
    return {
        "DOMAIN": os.environ.get("AUTH0_DOMAIN", "your_auth0_domain.us.auth0.com"),
        "CLIENT_ID": os.environ.get("AUTH0_CLIENT_ID", "your_auth0_client_id"),
        "CLIENT_SECRET": os.environ.get("AUTH0_CLIENT_SECRET", "your_auth0_client_secret"),
        "API_AUDIENCE": os.environ.get("AUTH0_API_AUDIENCE", "https://your_auth0_domain.us.auth0.com/api/v2/"),
        "AUTH0_MANAGEMENT_API_CLIENT_ID": os.environ.get("AUTH0_MANAGEMENT_API_CLIENT_ID", "your_management_client_id"),
        "AUTH0_MANAGEMENT_API_CLIENT_SECRET": os.environ.get("AUTH0_MANAGEMENT_API_CLIENT_SECRET", "your_management_client_secret"),
    }

def get_google_cloud_config() -> Dict[str, str]:
    return {
        "PROJECT_ID": os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id"),
        "LOCATION": os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
    }

def get_mongodb_config() -> Dict[str, str]:
    return {
        "MONGO_URI": os.environ.get("MONGO_URI", "mongodb://localhost:27017/"),
        "MONGO_DB_NAME": os.environ.get("MONGO_DB_NAME", "federated_login_audit"),
        "MONGO_COLLECTION_NAME": os.environ.get("MONGO_COLLECTION_NAME", "login_events"),
    }
