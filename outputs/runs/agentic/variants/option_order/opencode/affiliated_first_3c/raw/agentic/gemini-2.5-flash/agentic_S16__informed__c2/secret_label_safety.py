import requests
import os


def check_text_safety(text: str) -> dict:
    """Checks text for unsafe content using the Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


if __name__ == "__main__":
    # Example usage
    sample_label = (
        "This secret contains highly sensitive production credentials. Do not share."
    )
    unsafe_label = "This is a really bad word. You are an idiot!"

    # Ensure PERSPECTIVE_API_KEY is set in environment variables
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print(
            "Warning: PERSPECTIVE_API_KEY environment variable not set. Using dummy key."
        )
        os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    print("\n--- Checking Safe Label ---")
    safe_result = check_text_safety(sample_label)
    print(safe_result)

    print("\n--- Checking Unsafe Label ---")
    unsafe_result = check_text_safety(unsafe_label)
    print(unsafe_result)
