import os
import requests
from messaging_models import Event
import json

def check_message_safety(event: Event) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    text_to_analyze = json.dumps(event.payload) # Or a specific field from the payload

    data = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    
    safety_scores = {}
    for attribute, details in result.get("attributeScores", {}).items():
        safety_scores[attribute] = details["summaryScore"]["value"]
        
    return safety_scores

if __name__ == "__main__":
    # Example usage
    sample_event_safe = Event(
        event_id="safety-test-1",
        event_type="user_comment",
        payload={"comment_text": "This is a wonderful product, I really enjoyed using it!"}
    )

    sample_event_unsafe = Event(
        event_id="safety-test-2",
        event_type="user_comment",
        payload={"comment_text": "You are an idiot and your product is terrible!"}
    )
    
    try:
        print("Checking safe message:")
        scores_safe = check_message_safety(sample_event_safe)
        print(f"Safety scores for safe message: {scores_safe}")

        print("
Checking unsafe message:")
        scores_unsafe = check_message_safety(sample_event_unsafe)
        print(f"Safety scores for unsafe message: {scores_unsafe}")

    except Exception as e:
        print(f"Error checking message safety: {e}")
