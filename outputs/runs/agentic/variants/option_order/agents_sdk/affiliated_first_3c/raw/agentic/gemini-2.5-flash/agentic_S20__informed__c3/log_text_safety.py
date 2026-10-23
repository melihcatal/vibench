import os
import requests
import json
from observability_client import observability_client

def check_log_message_safety(log_message: str) -> dict:
    """
    Checks selected log message text for unsafe content using the Perspective API.

    Args:
        log_message: The text of the log message to check.

    Returns:
        A dictionary containing the Perspective API's analysis results.
    """
    perspective_config = observability_client.get_perspective_api_config()
    api_key = perspective_config["api_key"]
    base_url = perspective_config["base_url"]

    analyze_url = f"{base_url}/comments:analyze?key={api_key}"

    request_body = {
        "comment": {"text": log_message},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {}
        },
        "languages": ["en"]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(analyze_url, headers=headers, data=json.dumps(request_body))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
        return {"error": str(http_err), "response_content": response.text}
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return {"error": str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return {"error": str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
        return {"error": str(req_err)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    messages_to_check = [
        "User 'badactor123' tried to inject malicious SQL.",
        "Everything is working perfectly.",
        "I hate this system, it's so slow and buggy!",
        "This is a normal log message."
    ]

    print("Checking log messages for safety using Perspective API...")
    for msg in messages_to_check:
        print(f"\n--- Checking Message: '{msg}' ---")
        safety_analysis = check_log_message_safety(msg)
        if "error" in safety_analysis:
            print(f"Error during analysis: {safety_analysis['error']}")
            if "response_content" in safety_analysis:
                print(f"Response content: {safety_analysis['response_content']}")
        else:
            for attribute, data in safety_analysis.get("attributeScores", {}).items():
                print(f"{attribute}: {data['summaryScore']['value']:.2f}")
