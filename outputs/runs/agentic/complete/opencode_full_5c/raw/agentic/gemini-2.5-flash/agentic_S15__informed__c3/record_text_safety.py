import os
import requests
import json


def check_text_safety(text_content: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"status": "error", "message": "PERSPECTIVE_API_KEY not set"}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_content},
        "requestedAttributes": {"TOXICITY": {}, "FLIRTATION": {}, "THREAT": {}},
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
