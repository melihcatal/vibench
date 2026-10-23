import json
from security_client import get_perspective_api_config
import requests


def check_payload_safety(text: str) -> dict:
    config = get_perspective_api_config()
    api_key = config["api_key"]
    endpoint = config["endpoint"]

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{endpoint}?key={api_key}"

    # https://developers.perspectiveapi.com/s/docs-sample-requests
    request_payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, data=json.dumps(request_payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
