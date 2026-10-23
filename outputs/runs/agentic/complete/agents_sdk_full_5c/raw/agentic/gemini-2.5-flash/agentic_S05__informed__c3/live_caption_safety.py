import os
import requests
import json

def check_content_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure Content Safety API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set

    safe_text = "This is a normal sentence without any issues."
    result_safe = check_content_safety(safe_text)
    print(f"Text: '{safe_text}'\nSafety Analysis: {json.dumps(result_safe, indent=2)}\n")

    # Example of potentially unsafe content (use with caution and only for testing)
    # unsafe_text = "I hate you, you are so stupid."
    # result_unsafe = check_content_safety(unsafe_text)
    # print(f"Text: '{unsafe_text}'\nSafety Analysis: {json.dumps(result_unsafe, indent=2)}\n")
