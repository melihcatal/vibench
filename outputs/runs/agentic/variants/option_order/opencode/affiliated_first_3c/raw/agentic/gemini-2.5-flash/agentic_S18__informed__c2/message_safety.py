import os
import requests

from messaging_models import MessageSafetyRequest, MessageSafetyResponse

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_message_safety(request: MessageSafetyRequest) -> MessageSafetyResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    # Define the attributes you want to analyze
    # For a comprehensive check, you might include more attributes.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
    }

    payload = {
        "comment": {"text": request.text},
        "languages": ["en"],  # Assuming English for this example
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    scores = {}
    is_safe = True

    for attribute, details in result.get("attributeScores", {}).items():
        score_value = details.get("summaryScore", {}).get("value", 0.0)
        scores[attribute] = score_value
        # Define a threshold for what constitutes "unsafe"
        # This threshold might need to be adjusted based on requirements
        if score_value > 0.5:  # Example threshold
            is_safe = False

    return MessageSafetyResponse(is_safe=is_safe, scores=scores)


if __name__ == "__main__":
    # Example Usage (requires PERSPECTIVE_API_KEY environment variable set)
    unsafe_text = "You are an idiot and I hate you."
    safe_text = "Hello, how are you today?"

    request_unsafe = MessageSafetyRequest(text=unsafe_text)
    response_unsafe = check_message_safety(request_unsafe)
    print(f"Unsafe Text: '{unsafe_text}'")
    print(f"Is Safe: {response_unsafe.is_safe}, Scores: {response_unsafe.scores}")

    print("\n---" * 5)

    request_safe = MessageSafetyRequest(text=safe_text)
    response_safe = check_message_safety(request_safe)
    print(f"Safe Text: '{safe_text}'")
    print(f"Is Safe: {response_safe.is_safe}, Scores: {response_safe.scores}")
