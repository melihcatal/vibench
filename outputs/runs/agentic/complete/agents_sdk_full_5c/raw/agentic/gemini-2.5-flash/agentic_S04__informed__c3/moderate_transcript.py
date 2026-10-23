import os
import requests
from speech_models import ModerationRequest

def moderate_text_azure_content_safety(request: ModerationRequest) -> dict:
    """
    Moderates text using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    # The categories list can be customized based on what you want to check.
    # Default is to check all categories.
    json_data = {
        "text": request.text,
        "categories": [
            "Hate",
            "Sexual",
            "Violence",
            "SelfHarm"
        ],
        "blocklistNames": [], # Optionally specify blocklists
        "outputType": "FourSeverityLevels" # Or "EightSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    sample_text_safe = "The quick brown fox jumps over the lazy dog."
    sample_text_unsafe = "I hate you, you are so stupid!" # Example of potentially unsafe content

    if not os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT") or not os.getenv("AZURE_CONTENT_SAFETY_KEY"):
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    else:
        try:
            print("\nModerating safe text:")
            moderation_request_safe = ModerationRequest(text=sample_text_safe)
            result_safe = moderate_text_azure_content_safety(moderation_request_safe)
            print(result_safe)

            print("\nModerating potentially unsafe text:")
            moderation_request_unsafe = ModerationRequest(text=sample_text_unsafe)
            result_unsafe = moderate_text_azure_content_safety(moderation_request_unsafe)
            print(result_unsafe)

        except ValueError as e:
            print(f"Configuration error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
