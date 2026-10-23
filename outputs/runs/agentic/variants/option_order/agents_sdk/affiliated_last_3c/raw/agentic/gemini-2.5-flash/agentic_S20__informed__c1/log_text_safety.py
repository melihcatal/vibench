import os
import requests
import json

def check_log_text_safety(log_message: str) -> dict:
    """
    Checks the safety of a log message using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        return {"error": "Azure Content Safety endpoint or key not set in environment variables."}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": log_message,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "breakByBlocklists": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling Azure AI Content Safety API: {e}"}

if __name__ == "__main__":
    test_message_safe = "User accessed resource successfully."
    test_message_unsafe = "User attempted to post hate speech." # Example of potentially unsafe content

    print(f"Checking safety for: '{test_message_safe}'")
    result_safe = check_log_text_safety(test_message_safe)
    print(json.dumps(result_safe, indent=2))

    print(f"\nChecking safety for: '{test_message_unsafe}'")
    result_unsafe = check_log_text_safety(test_message_unsafe)
    print(json.dumps(result_unsafe, indent=2))
