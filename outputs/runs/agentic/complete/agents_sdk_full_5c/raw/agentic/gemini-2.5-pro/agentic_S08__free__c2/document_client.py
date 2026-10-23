import os
from typing import Dict, Optional

def get_google_credentials():
    """Placeholder for getting Google Cloud credentials."""
    # In a real app, this would use google.auth.default() or similar
    # For this example, we assume env vars are set for application-default credentials
    return None

def get_aws_credentials() -> Dict[str, str]:
    """Loads AWS credentials from environment variables."""
    return {
        "access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "region": os.environ.get("AWS_REGION", "us-east-1"),
    }

def get_mongo_connection_string() -> Optional[str]:
    """Loads MongoDB connection string from environment variables."""
    return os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
