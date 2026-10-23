import os
import requests


def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Example of a simplified request for TOXICITY
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety: {e}")
        return {"error": str(e)}
