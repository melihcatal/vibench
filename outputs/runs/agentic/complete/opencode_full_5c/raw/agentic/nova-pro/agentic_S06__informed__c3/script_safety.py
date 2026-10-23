import os
import requests

# Set up the Perspective API client
perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")


def check_script_safety(script):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": perspective_api_key,
    }
    data = {
        "comment": {"text": script},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params=params, json=data)
    return response.json()
