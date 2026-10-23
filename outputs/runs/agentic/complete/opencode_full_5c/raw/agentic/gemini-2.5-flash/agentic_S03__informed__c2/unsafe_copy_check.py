import requests
import os


def check_unsafe_content(text: str) -> dict:
    """Checks localized copy for unsafe content using the Perspective API.
    The PERSPECTIVE_API_KEY environment variable must be set.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Specify the attributes to analyze
    attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": attributes,
        "languages": [
            "en"
        ],  # Perspective API supports multiple languages, but 'en' is common
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    return response.json()


if __name__ == "__main__":
    os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    text_to_check = "This is a great comment!"
    safety_report = check_unsafe_content(text_to_check)
    print(f"Safety Report: {safety_report}")

    unsafe_text = "You are an idiot!"
    unsafe_safety_report = check_unsafe_content(unsafe_text)
    print(f"Unsafe Safety Report: {unsafe_safety_report}")
