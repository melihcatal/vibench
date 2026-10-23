import os
import requests


def check_live_caption_safety(text: str, api_key: str = None) -> dict:
    """
    Checks live transcript text for unsafe content using the Perspective API.

    Args:
        text (str): The text content to analyze.
        api_key (str): Your Perspective API key. If None, it will try to get it from PERSPECTIVE_API_KEY env var.

    Returns:
        dict: A dictionary containing the analysis results from Perspective API.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "Perspective API key not provided and PERSPECTIVE_API_KEY env var is not set."
        )

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Request body for analysis
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": [
            "en"
        ],  # Specify language if known, otherwise omit for auto-detection
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        print(f"Perspective API analysis for '{text}': {result}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # Make sure to set PERSPECTIVE_API_KEY environment variable
    # os.environ["PERSPECTIVE_API_KEY"] = "your-perspective-api-key"
    # try:
    #     safety_results = check_live_caption_safety("You are an idiot!")
    #     print(f"Safety check results: {safety_results}")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
