import os
import requests
import json

# Perspective API Endpoint and Key
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
# Ensure PERSPECTIVE_API_KEY environment variable is set
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def check_message_safety(text_payload: str) -> dict:
    """Checks message payload text for unsafe content using Perspective API."""
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {}
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_result = response.json()
        
        # Extract scores for common safety attributes
        safety_scores = {}
        for attr, details in analysis_result.get("attributeScores", {}).items():
            score = details.get("summaryScore", {}).get("value")
            if score is not None:
                safety_scores[attr] = score
                
        return {"success": True, "scores": safety_scores, "raw_response": analysis_result}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Perspective API request failed: {e}"}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    # Example usage
    # export PERSPECTIVE_API_KEY="your-perspective-api-key"
    # python message_safety.py
    
    safe_text = "This is a perfectly fine message."
    unsafe_text = "You are an idiot! I hate you."

    print(f"\nChecking safety for: '{safe_text}'")
    result_safe = check_message_safety(safe_text)
    print(json.dumps(result_safe, indent=2))

    print(f"\nChecking safety for: '{unsafe_text}'")
    result_unsafe = check_message_safety(unsafe_text)
    print(json.dumps(result_unsafe, indent=2))
