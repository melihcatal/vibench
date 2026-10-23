import os
import requests
import json

def check_payload_safety(text_payload: str, client_ip: str = "127.0.0.1") -> dict:
    """
    Checks decrypted text payloads for unsafe content using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "spanAnnotations": False,
        "doNotStore": True,
        "clientToken": client_ip # Can be used for rate limiting/abuse prevention
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        
        summary = {
            "text": text_payload,
            "is_safe": True,
            "scores": {}
        }
        
        for attribute, details in result.get("attributeScores", {}).items():
            score = details.get("summaryScore", {}).get("value")
            if score is not None:
                summary["scores"][attribute] = score
                # Define a threshold for "unsafe". This is an example, adjust as needed.
                if attribute == "TOXICITY" and score > 0.7:
                    summary["is_safe"] = False
        
        return summary

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"text": text_payload, "is_safe": False, "error": str(e), "scores": {}}
