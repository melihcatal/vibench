import os
from dotenv import load_dotenv
import requests

load_dotenv()

DOPPLER_TOKEN = os.getenv("DOPPLER_TOKEN")
BASE_URL = "https://platform.doppler.com/v1/secrets/get"


def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from Doppler Secrets using the Doppler REST API.

    Returns the secret value as a string.
    """
    headers = {
        "Authorization": f"Bearer {DOPPLER_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"name": secret_name}
    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["value"]
