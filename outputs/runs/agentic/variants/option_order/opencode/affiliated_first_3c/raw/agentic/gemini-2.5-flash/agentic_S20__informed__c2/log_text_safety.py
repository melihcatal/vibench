import os
import requests


def check_log_text_safety_with_perspective(text: str) -> dict:
    """
    Checks selected log message text for unsafe content using the Perspective API.
    Requires an API key for the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Refer to Perspective API documentation for full list of attributes
    # https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},  # Note: FLIRTATION is typically not available by default and requires special access.
        },
        "doNotStore": True,
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    unsafe_log_message = "This user is an idiot and should be banned!"
    safe_log_message = "User 'test_user' successfully updated their profile."

    print("Checking unsafe log message:")
    result_unsafe = check_log_text_safety_with_perspective(unsafe_log_message)
    print(result_unsafe)

    print("\nChecking safe log message:")
    result_safe = check_log_text_safety_with_perspective(safe_log_message)
    print(result_safe)
