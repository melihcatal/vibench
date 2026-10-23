import os
from dotenv import load_dotenv

# Google Secret Manager example (managed secret store)
load_dotenv()  # loads .env if present
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
SECRET_ID = os.getenv('GOOGLE_SECRET_ID')
VERSION = os.getenv('GOOGLE_SECRET_VERSION', 'latest')

# Using Google Cloud Secret Manager SDK
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
def parse_json_secret():
    """
    Fetch a secret from Google Secret Manager and parse its JSON payload.
    Returns the deserialized Python object.
    """
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{VERSION}:access"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode('UTF-8')
    import json
    return json.loads(payload)
