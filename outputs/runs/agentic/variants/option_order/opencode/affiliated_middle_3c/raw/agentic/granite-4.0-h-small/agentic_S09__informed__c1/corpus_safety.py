import os
import requests  # placeholder; replace with actual SDK if using another provider


def is_safe(text: str) -> bool:
    """
    Check whether the provided text passes content safety filters.

    Args:
        text (str): Corpus text to evaluate.

    Returns:
        bool: True if safe, False otherwise.
    """
    # Example using AWS Comprehend toxicity detection (replace with real SDK as needed)
    endpoint_url = os.getenv("AWS_COMPREHEND_ENDPOINT")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    # Dummy request payload; adapt to actual API schema
    payload = {"text": text}
    response = requests.post(endpoint_url, json=payload, auth=(access_key, secret_key))
    # Assume response JSON contains {'toxic': false} for safe content
    result = response.json()
    return not result.get("toxic", False)
