import os
import requests
from observability_models import SafetyCheckRequest

# Google Cloud Perspective API endpoint
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_log_text_safety(safety_request: SafetyCheckRequest) -> dict:
    """
    Checks selected log message text for unsafe content using Google Cloud Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set for Perspective API.")

    payload = {
        "comment": {"text": safety_request.text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"],
    }

    if safety_request.client_ip:
        payload["context"] = {"entries": [{"type": "IP_ADDRESS", "value": safety_request.client_ip}]}
    if safety_request.session_id:
        if "context" not in payload:
            payload["context"] = {"entries": []}
        payload["context"]["entries"].append({"type": "WEB_SESSION_ID", "value": safety_request.session_id})

    params = {"key": api_key}

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example log messages
    log_message_1 = "User 'bad_actor' tried to inject malicious script: <script>alert('xss');</script>"
    log_message_2 = "This is a normal log message from user 'good_user'."
    log_message_3 = "Alert! Unauthorized access attempt detected from a suspicious IP."
    log_message_4 = "That user is a total idiot, ban them immediately!" # Example of potentially toxic content

    print("--- Checking safety for log_message_1 ---")
    safety_req_1 = SafetyCheckRequest(text_content=log_message_1, client_ip="192.0.2.1")
    result_1 = check_log_text_safety(safety_req_1)
    print(result_1)

    print("\n--- Checking safety for log_message_2 ---")
    safety_req_2 = SafetyCheckRequest(text_content=log_message_2)
    result_2 = check_log_text_safety(safety_req_2)
    print(result_2)

    print("\n--- Checking safety for log_message_3 ---")
    safety_req_3 = SafetyCheckRequest(text_content=log_message_3)
    result_3 = check_log_text_safety(safety_req_3)
    print(result_3)
    
    print("\n--- Checking safety for log_message_4 (potentially toxic) ---")
    safety_req_4 = SafetyCheckRequest(text_content=log_message_4)
    result_4 = check_log_text_safety(safety_req_4)
    print(result_4)
