import os
import requests

def unsafe_copy_check(texts: List[str]) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []

    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {}
            }
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            results.append(response.json())
        else:
            results.append({"error": response.text})

    return {"unsafe_check_results": results}