import os
import requests
import json


def check_content_safety(text: str, endpoint: str, key: str):
    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return None


if __name__ == "__main__":
    azure_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if azure_endpoint and azure_key:
        test_text_safe = "This is a normal and safe sentence."
        test_text_unsafe = "I hate you so much, I want to hurt you."

        print("Checking safe text...")
        safety_report_safe = check_content_safety(
            test_text_safe, azure_endpoint, azure_key
        )
        print(json.dumps(safety_report_safe, indent=2))

        print("\nChecking unsafe text...")
        safety_report_unsafe = check_content_safety(
            test_text_unsafe, azure_endpoint, azure_key
        )
        print(json.dumps(safety_report_unsafe, indent=2))
    else:
        print(
            "Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )
