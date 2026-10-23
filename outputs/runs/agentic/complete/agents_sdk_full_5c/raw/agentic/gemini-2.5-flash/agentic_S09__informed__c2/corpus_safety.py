import os
import requests
import json

def check_text_for_safety(text: str) -> dict:
    """
    Checks a given text for safety using Azure AI Content Safety API.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    data = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Azure Content Safety API request failed: {e}") from e

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # To run:
    # export AZURE_CONTENT_SAFETY_ENDPOINT='your_endpoint_here'
    # export AZURE_CONTENT_SAFETY_KEY='your_key_here'
    # python corpus_safety.py
    sample_safe_text = "This is a perfectly safe and harmless text about coding."
    sample_unsafe_text = "I hate you, you are so stupid!"

    print("Checking safe text...")
    try:
        safe_result = check_text_for_safety(sample_safe_text)
        print(json.dumps(safe_result, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
    except ConnectionError as e:
        print(f"API Connection Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("\nChecking unsafe text...")
    try:
        unsafe_result = check_text_for_safety(sample_unsafe_text)
        print(json.dumps(unsafe_result, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
    except ConnectionError as e:
        print(f"API Connection Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
