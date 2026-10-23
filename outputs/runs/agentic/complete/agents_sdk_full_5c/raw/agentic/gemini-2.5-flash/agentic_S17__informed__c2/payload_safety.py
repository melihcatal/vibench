import os
import requests

from security_models import ContentSafetyRequest, ContentSafetyResult

# Perspective API hostname
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_payload_safety(request: ContentSafetyRequest) -> ContentSafetyResult:
    """Checks decrypted text payloads for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {
        "key": api_key
    }
    payload = {
        "comment": {"text": request.text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload)
        response.raise_for_status()
        analysis_result = response.json()

        scores = {}
        unsafe_categories = []
        is_safe = True

        for attr, data in analysis_result.get("attributeScores", {}).items():
            score = data.get("summaryScore", {}).get("value", 0.0)
            scores[attr] = score
            # Define a threshold for what's considered unsafe. This is an example.
            if score > 0.7:
                is_safe = False
                unsafe_categories.append(attr)
        
        return ContentSafetyResult(is_safe=is_safe, scores=scores, unsafe_categories=unsafe_categories)

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return ContentSafetyResult(is_safe=False, scores={}, unsafe_categories=["API_ERROR"])

if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY env var)
    # from dotenv import load_dotenv
    # load_dotenv()
    # 
    # safe_text_req = ContentSafetyRequest(text_content="This is a perfectly normal sentence.")
    # safe_result = check_payload_safety(safe_text_req)
    # print(f"Safe Text Result: {safe_result}")
    #
    # unsafe_text_req = ContentSafetyRequest(text_content="You are an idiot!")
    # unsafe_result = check_payload_safety(unsafe_text_req)
    # print(f"Unsafe Text Result: {unsafe_result}")
    pass
