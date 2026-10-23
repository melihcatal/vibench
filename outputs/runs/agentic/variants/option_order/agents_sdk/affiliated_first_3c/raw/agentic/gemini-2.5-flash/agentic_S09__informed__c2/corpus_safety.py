import os
import requests

def check_corpus_safety(text: str) -> dict:
    """Checks the safety of a given text using the Perspective API.

    Args:
        text: The text string to check.

    Returns:
        A dictionary containing the Perspective API analysis results.
        Returns an empty dict if the API key is not set or request fails.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        print("PERSPECTIVE_API_KEY environment variable not set. Skipping safety check.")
        return {}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # The request body specifies the text and the attributes to analyze.
    # Common attributes include TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, etc.
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'THREAT': {},
            'INSULT': {},
            'PROFANE': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
            'ATTACK_ON_AUTHOR': {},
            'ATTACK_ON_COMMENTER': {},
        }
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {}

if __name__ == '__main__':
    # Example usage (ensure PERSPECTIVE_API_KEY is set in environment variables)
    # from dotenv import load_dotenv
    # load_dotenv()

    # safe_text = "This is a perfectly normal and polite sentence."
    # unsafe_text = "You are an idiot! I hate you!"

    # print("\nChecking safe text:")
    # safety_report_safe = check_corpus_safety(safe_text)
    # if safety_report_safe:
    #     print(safety_report_safe)

    # print("\nChecking unsafe text:")
    # safety_report_unsafe = check_corpus_safety(unsafe_text)
    # if safety_report_unsafe:
    #     print(safety_report_unsafe)
    pass
