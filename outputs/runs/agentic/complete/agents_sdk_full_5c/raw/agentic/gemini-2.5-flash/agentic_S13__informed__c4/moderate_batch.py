import os
import requests
import json

def moderate_batch(texts: list[str]):
    """Moderates a batch of user messages and returns per-message decisions using Tisane."""
    api_key = os.environ["TISANE_API_KEY"]
    tisane_endpoint = "https://api.tisane.ai/parse"

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
    }

    results = []
    for text in texts:
        payload = {
            "language": "en", # Assuming English for this example
            "text": text,
            "settings": {
                "sentiment": True,
                "document_level_sentiment": True
            }
        }
        try:
            response = requests.post(tisane_endpoint, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            results.append({
                "text": text,
                "tisane_response": response.json()
            })
        except requests.exceptions.RequestException as e:
            print(f"Error moderating text batch with Tisane: {e}")
            results.append({
                "text": text,
                "error": str(e)
            })
    return results
