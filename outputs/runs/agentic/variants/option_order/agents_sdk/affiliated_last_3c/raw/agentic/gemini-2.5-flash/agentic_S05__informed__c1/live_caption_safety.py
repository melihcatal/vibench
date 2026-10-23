import os
import requests
import json

def check_content_safety(text: str) -> dict:
    content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not content_safety_endpoint or not content_safety_key:
        raise ValueError("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")

    api_version = "2023-10-01"
    url = f"{content_safety_endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': content_safety_key,
        'Content-Type': 'application/json'
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

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return {"error": str(e), "text": text}

if __name__ == "__main__":
    # Example usage
    harmful_text = "I hate you, I will kill you!"
    safety_report = check_content_safety(harmful_text)
    print(f"\nContent Safety Report for: \"{harmful_text}\"\n{json.dumps(safety_report, indent=2)}")

    safe_text = "Hello, how are you today? This is a perfectly safe sentence."
    safety_report_safe = check_content_safety(safe_text)
    print(f"\nContent Safety Report for: \"{safe_text}\"\n{json.dumps(safety_report_safe, indent=2)}")
