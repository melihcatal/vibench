import requests
import json
import os
from observability_client import get_azure_content_safety_config


def check_text_safety(log_message: str) -> dict:
    """Checks selected log message text for unsafe content using Azure AI Content Safety."""
    config = get_azure_content_safety_config()
    endpoint = config["endpoint"]
    key = config["key"]

    # The Text Analysis API endpoint
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    data = {
        "text": log_message,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    print(f"Sending log message to Azure AI Content Safety: {log_message[:50]}...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        safety_results = response.json()
        print("Azure AI Content Safety check completed.")
        return safety_results
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety: {e}")
        return {
            "error": str(e),
            "message": "Failed to connect to Azure AI Content Safety.",
        }


if __name__ == "__main__":
    # Example usage:
    test_message_1 = "This is a normal log message with no issues."
    results_1 = check_text_safety(test_message_1)
    print("\n--- Safety Check Results 1 ---")
    print(json.dumps(results_1, indent=2))

    # Example of potentially unsafe content (replace with actual test cases for full evaluation)
    # Note: The exact detection depends on Azure's models and configuration.
    test_message_2 = "I will harm myself now."
    results_2 = check_text_safety(test_message_2)
    print("\n--- Safety Check Results 2 ---")
    print(json.dumps(results_2, indent=2))

    test_message_3 = "I hate this user and want them gone."
    results_3 = check_text_safety(test_message_3)
    print("\n--- Safety Check Results 3 ---")
    print(json.dumps(results_3, indent=2))
