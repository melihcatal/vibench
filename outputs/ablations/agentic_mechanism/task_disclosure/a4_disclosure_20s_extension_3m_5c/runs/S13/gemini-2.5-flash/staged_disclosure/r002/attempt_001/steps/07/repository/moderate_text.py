from googleapiclient import discovery
import json
import os

def moderate_text(text):
    API_KEY = os.environ.get('PERSPECTIVE_API_KEY') # User needs to set this environment variable
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=API_KEY,
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

if __name__ == '__main__':
    user_text = input("Enter text to moderate: ")
    result = moderate_text(user_text)
    print(json.dumps(result, indent=2))
