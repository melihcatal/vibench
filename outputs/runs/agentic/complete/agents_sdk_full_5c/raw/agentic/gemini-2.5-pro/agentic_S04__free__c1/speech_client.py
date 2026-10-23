import os
import requests

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")
ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"

if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

def get_assemblyai_headers():
    """Returns authorization headers for AssemblyAI API."""
    return {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

def post_to_assemblyai(endpoint: str, data: dict):
    """Submits a POST request to the AssemblyAI API."""
    url = f"{ASSEMBLYAI_API_BASE}/{endpoint}"
    response = requests.post(url, json=data, headers=get_assemblyai_headers())
    response.raise_for_status()
    return response.json()

def get_from_assemblyai(endpoint: str):
    """Submits a GET request to the AssemblyAI API."""
    url = f"{ASSEMBLYAI_API_BASE}/{endpoint}"
    response = requests.get(url, headers=get_assemblyai_headers())
    response.raise_for_status()
    return response.json()
