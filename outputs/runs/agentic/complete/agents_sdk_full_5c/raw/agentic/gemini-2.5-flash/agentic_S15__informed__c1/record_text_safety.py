import os
import requests
import json

def check_text_safety(text_content: str) -> dict:
    """
    Checks the safety of text content using the Perspective API.
    """
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    
    request_body = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(request_body))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        analysis_results = response.json()
        print(f"Perspective API analysis for text: '{text_content}' -> {analysis_results}")
        return analysis_results
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Set PERSPECTIVE_API_KEY environment variable for testing
    
    # Example 1: Relatively safe text
    safe_text = "This is a wonderful product, I really enjoyed using it!"
    safety_report_safe = check_text_safety(safe_text)
    print(f"Safety report for safe text: {safety_report_safe}")

    # Example 2: Potentially unsafe text
    unsafe_text = "You are an idiot and your work is trash. I will make sure you regret this!"
    safety_report_unsafe = check_text_safety(unsafe_text)
    print(f"Safety report for unsafe text: {safety_report_unsafe}")
