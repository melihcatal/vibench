import requests
import os

# Perspective API endpoint and model
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_content_safety(text: str, api_key: str = None) -> dict:
    """Checks text for unsafe content using Google's Perspective API.

    Args:
        text: The text content to analyze.
        api_key: Your Perspective API key. If None, it tries to get from environment variable.

    Returns:
        A dictionary containing the analysis results, including scores for different attributes.
        Returns an empty dict if API key is missing or an error occurs.
    """
    if not text.strip():
        return {"errors": "Input text is empty."}

    if api_key is None:
        api_key = os.getenv("PERSPECTIVE_API_KEY")

    if not api_key:
        print("Error: PERSPECTIVE_API_KEY environment variable not set or provided.")
        return {"errors": "PERSPECTIVE_API_KEY is missing."}

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"
    
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    # for available attributes.
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            # "SEXUALLY_EXPLICIT": {},
            # "FLIRTATION": {},
            # "SPAM": {},
        },
        "languages": ["en"],
        "doNotStore": True # Set to True for live/real-time content that should not be stored.
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_results = response.json()
        return analysis_results
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"errors": str(e)}

if __name__ == "__main__":
    # Ensure PERSPECTIVE_API_KEY is set in your environment variables
    # You can get an API key from https://perspectiveapi.com/

    print("\n--- Testing with benign text ---")
    benign_text = "This is a perfectly normal sentence."
    results = check_content_safety(benign_text)
    if "errors" not in results:
        print(f"Text: '{benign_text}'")
        for attribute, score_data in results.get("attributeScores", {}).items():
            print(f"  {attribute}: {score_data['summaryScore']['value']:.2f}")
    else:
        print(f"Failed to analyze: {results['errors']}")

    print("\n--- Testing with potentially toxic text ---")
    toxic_text = "You are an idiot and I hate you!"
    results = check_content_safety(toxic_text)
    if "errors" not in results:
        print(f"Text: '{toxic_text}'")
        for attribute, score_data in results.get("attributeScores", {}).items():
            print(f"  {attribute}: {score_data['summaryScore']['value']:.2f}")
    else:
        print(f"Failed to analyze: {results['errors']}")

    print("\n--- Testing with another potentially toxic text ---")
    toxic_text_2 = "This is the worst product ever. It's a complete scam!"
    results = check_content_safety(toxic_text_2)
    if "errors" not in results:
        print(f"Text: '{toxic_text_2}'")
        for attribute, score_data in results.get("attributeScores", {}).items():
            print(f"  {attribute}: {score_data['summaryScore']['value']:.2f}")
    else:
        print(f"Failed to analyze: {results['errors']}")
