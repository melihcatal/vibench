import os
import requests
import json

# Azure AI Content Safety
# https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview

def check_text_for_safety(text: str, endpoint: str, key: str) -> dict:
    """Checks text for unsafe content using Azure AI Content Safety."""
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    body = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    return response.json()

def check_secret_labels_safety(secret_name: str, labels: dict, notes: str = None) -> dict:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety.
    Returns a dictionary of safety results for each checked field.
    """
    azure_cs_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_cs_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not azure_cs_endpoint or not azure_cs_key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    safety_results = {"secret_name": secret_name}

    # Check labels
    for key, value in labels.items():
        combined_label_text = f"{key}: {value}"
        try:
            label_safety = check_text_for_safety(combined_label_text, azure_cs_endpoint, azure_cs_key)
            safety_results[f"label_safety_{key}"] = label_safety
        except Exception as e:
            safety_results[f"label_safety_{key}_error"] = str(e)

    # Check notes if provided
    if notes:
        try:
            notes_safety = check_text_for_safety(notes, azure_cs_endpoint, azure_cs_key)
            safety_results["notes_safety"] = notes_safety
        except Exception as e:
            safety_results["notes_safety_error"] = str(e)

    return safety_results

if __name__ == "__main__":
    # Example usage
    test_secret_labels = {
        "environment": "production",
        "department": "engineering",
        "sensitive_info": "contains-PII-data"
    }
    test_secret_notes = "This secret is critical for payment processing. Handle with extreme care. Do not log its content."
    test_secret_name = "app-payments-api-key"

    try:
        safety_report = check_secret_labels_safety(test_secret_name, test_secret_labels, test_secret_notes)
        print(json.dumps(safety_report, indent=2))

        # Example with potentially unsafe content
        unsafe_labels = {"project": "evil-plans", "category": "violence-related"}
        unsafe_notes = "Destroy all competitors immediately with extreme prejudice."
        unsafe_secret_name = "illegal-operation-secret"
        unsafe_report = check_secret_labels_safety(unsafe_secret_name, unsafe_labels, unsafe_notes)
        print(f"\n--- Unsafe Content Check ---\n{json.dumps(unsafe_report, indent=2)}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during safety check: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
