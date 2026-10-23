import os
import requests

# Perspective API endpoint
# Refer to: https://developers.perspectiveapi.com/s/docs-sample-code
PERSPECTIVE_API_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
)


def record_text_safety(text_content: str):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "message": "PERSPECTIVE_API_KEY environment variable not set.",
        }

    url = PERSPECTIVE_API_URL + api_key
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_content},
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
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return {"status": "success", "analysis": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
