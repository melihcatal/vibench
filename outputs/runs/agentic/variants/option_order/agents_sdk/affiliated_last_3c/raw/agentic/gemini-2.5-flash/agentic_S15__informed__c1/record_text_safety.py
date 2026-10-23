import os
import requests

def check_text_safety(text_content: str, api_key: str | None = None) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API.

    Args:
        text_content: The text string to analyze for safety.
        api_key: Your Perspective API key. If None, it will try to read from PERSPECTIVE_API_KEY environment variable.

    Returns:
        A dictionary containing the safety analysis results.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("Perspective API key not provided and not found in environment variable PERSPECTIVE_API_KEY.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # The request body for Perspective API. Customize attributes as needed.
    request_body = {
        'comment': {'text': text_content},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        }
    }

    try:
        response = requests.post(api_url, json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_result = response.json()
        print(f"Perspective API analysis completed for text of length {len(text_content)}.")
        return analysis_result
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety with Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY environment variable)
    # sample_text = "This is a perfectly normal and polite comment."
    # unsafe_text = "You are an idiot and I hate you!"
    #
    # if os.environ.get("PERSPECTIVE_API_KEY"):
    #     print("\nAnalyzing safe text:")
    #     safe_analysis = check_text_safety(sample_text)
    #     print(safe_analysis)
    #
    #     print("\nAnalyzing unsafe text:")
    #     unsafe_analysis = check_text_safety(unsafe_text)
    #     print(unsafe_analysis)
    # else:
    #     print("Please set the PERSPECTIVE_API_KEY environment variable to run the example.")
    pass
