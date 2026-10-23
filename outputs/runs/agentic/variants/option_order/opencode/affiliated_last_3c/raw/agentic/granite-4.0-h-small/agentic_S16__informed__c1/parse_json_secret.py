import json
import os
from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

client = secretmanager.SecretManagerServiceClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def fetch_json_secret(secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret from Google Secret Manager.

    Returns the parsed JSON object.
    """
    name = client.secret_path(PROJECT_ID, secret_name)
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)
