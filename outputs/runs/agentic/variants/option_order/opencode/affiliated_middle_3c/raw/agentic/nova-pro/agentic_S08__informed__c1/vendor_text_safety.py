import os
import requests


def moderate_vendor_text(vendor_text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": vendor_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "spanAnnotations": False,
    }
    response = requests.post(url, headers=headers, json=data, params={"key": api_key})
    return response.json()
