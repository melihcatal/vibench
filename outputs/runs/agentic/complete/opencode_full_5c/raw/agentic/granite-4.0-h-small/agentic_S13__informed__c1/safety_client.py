import os
import requests


def fetch(api_key: str, request_body: dict) -> dict:
    """Core call to Perspective API."""
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"X-Goog-Api-Key": api_key, "Content-Type": "application/json"}
    response = requests.post(url, json=request_body, headers=headers)
    response.raise_for_status()
    return response.json()


# Example usage helper (not part of public API)
if __name__ == "__main__":
    text = "This is a test comment.\nIt may contain toxic language."
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    result = fetch(
        api_key, {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    )
    print(result)
