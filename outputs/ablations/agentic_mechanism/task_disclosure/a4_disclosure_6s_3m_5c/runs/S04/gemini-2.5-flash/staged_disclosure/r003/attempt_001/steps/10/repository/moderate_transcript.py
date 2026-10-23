from googleapiclient import discovery
import json
import os

def moderate_text(text):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        static_discovery=False,
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
    transcript_text = "This is an example transcript with some potentially harmful content."
    moderation_results = moderate_text(transcript_text)
    print(json.dumps(moderation_results, indent=2))
