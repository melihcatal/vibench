import os
import requests
import json

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_batch(texts: list[str]):
    results = []
    for text in texts:
        url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
        data = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "THREAT": {},
                "INSULT": {},
                "PROFANITY": {},
            },
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        results.append(response.json())
    return results
