import os
import requests

def check_unsafe_content(text: str, client_ip: str = None) -> dict:
    """Checks localized copy for unsafe content using Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key

    # https://developers.perspectiveapi.com/s/about-the-api
    # A request that evaluates the toxicity and other attributes of a comment.
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        },
        'languages': ['en'] # Perspective API supports various languages, specify as needed
    }

    if client_ip:
        data['clientToken'] = client_ip # Can be used for rate limiting or abuse detection

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Set PERSPECTIVE_API_KEY environment variable
    # A Google Cloud API Key with Perspective API enabled.
    text_to_check = "You are an idiot and I hate you!"
    safety_report = check_unsafe_content(text_to_check)
    print(f"Safety Report for \"{text_to_check}\" :\n{safety_report}")

    text_clean = "This is a perfectly safe sentence."
    safety_report_clean = check_unsafe_content(text_clean)
    print(f"\nSafety Report for \"{text_clean}\" :\n{safety_report_clean}")
