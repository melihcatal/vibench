import os
import requests
import json

# Perspective API endpoint
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_content_safety(text: str, api_key: str, threshold: float = 0.8) -> dict:
    """Checks live transcript text for unsafe content using the Perspective API.

    Args:
        text (str): The transcript text to analyze.
        api_key (str): Your Perspective API key.
        threshold (float): The threshold for flagging content as unsafe (0.0 to 1.0).

    Returns:
        dict: A dictionary containing safety analysis results, including a boolean
              `is_unsafe` if any attribute exceeds the threshold.
    """
    if not text.strip():
        return {"text": text, "is_unsafe": False, "scores": {}}

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # List of attributes to analyze. You can add more as needed.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "doNotStore": True # Set to True for live/production use cases where you don't want data stored
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        
        analysis_scores = {}
        is_unsafe = False

        for attribute, details in result.get("attributeScores", {}).items():
            score = details.get("summaryScore", {}).get("value", 0.0)
            analysis_scores[attribute] = score
            if score > threshold:
                is_unsafe = True
        
        print(f"Content Safety Check for '{text}':")
        for attr, score in analysis_scores.items():
            print(f"  {attr}: {score:.4f}")
        if is_unsafe:
            print(f"  -> Content is potentially UNSAFE (exceeds threshold {threshold:.2f})")
        else:
            print(f"  -> Content is considered SAFE (below threshold {threshold:.2f})")

        return {"text": text, "is_unsafe": is_unsafe, "scores": analysis_scores}

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Perspective API: {e}")
        return {"text": text, "is_unsafe": False, "error": str(e), "scores": {}}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Perspective API response: {response.text}")
        return {"text": text, "is_unsafe": False, "error": "Invalid JSON response", "scores": {}}


if __name__ == "__main__":
    # To run this, ensure PERSPECTIVE_API_KEY is set.
    # export PERSPECTIVE_API_KEY="YOUR_PERSPECTIVE_API_KEY"
    print("Live caption safety check using Perspective API.")

    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        print("Error: PERSPECTIVE_API_KEY environment variable not set.")
    else:
        print("\n--- Checking safe content ---")
        safe_text = "This is a perfectly normal and friendly conversation."
        safety_results_safe = check_content_safety(safe_text, perspective_api_key)
        
        print("\n--- Checking potentially unsafe content (insult) ---")
        unsafe_text_1 = "You are an idiot and I hate you."
        safety_results_unsafe_1 = check_content_safety(unsafe_text_1, perspective_api_key)

        print("\n--- Checking potentially unsafe content (threat) ---")
        unsafe_text_2 = "I will hurt you if you say that again."
        safety_results_unsafe_2 = check_content_safety(unsafe_text_2, perspective_api_key, threshold=0.7)

    print("Ensure PERSPECTIVE_API_KEY is set for execution.")
