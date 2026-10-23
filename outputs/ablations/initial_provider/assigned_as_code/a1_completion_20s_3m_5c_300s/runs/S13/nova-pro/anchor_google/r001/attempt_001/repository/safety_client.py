import os

import requests


def get_client(config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key is required")
    return requests.Session()