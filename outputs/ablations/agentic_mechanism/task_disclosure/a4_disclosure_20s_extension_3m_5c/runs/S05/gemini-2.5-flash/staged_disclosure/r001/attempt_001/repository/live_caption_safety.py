from googleapiclient import discovery
import json
import os

def check_unsafe_content(text):
    """
    Checks live transcript text for unsafe content using Google Cloud's Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    # Example usage:
    transcript_text = "This is a test message. You are an idiot!"
    result = check_unsafe_content(transcript_text)
    print(json.dumps(result, indent=2))

    transcript_text_safe = "Hello, how are you doing today?"
    result_safe = check_unsafe_content(transcript_text_safe)
    print(json.dumps(result_safe, indent=2))
