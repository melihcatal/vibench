import os
import requests


def check_text_safety(text: str):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "message": "PERSPECTIVE_API_KEY not found in environment variables.",
        }

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {"status": "success", "analysis": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
