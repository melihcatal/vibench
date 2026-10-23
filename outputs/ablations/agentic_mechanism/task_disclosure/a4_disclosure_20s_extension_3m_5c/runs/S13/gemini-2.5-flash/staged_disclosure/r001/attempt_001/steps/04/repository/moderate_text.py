import os
import googleapiclient.discovery

def moderate_text(text: str) -> dict:
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = googleapiclient.discovery.build(
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
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    test_text = "You are a horrible person!"
    scores = moderate_text(test_text)
    print(f"Moderation scores for '{test_text}':")
    for attribute, value in scores.get("attributeScores", {}).items():
        print(f"  {attribute}: {value['summaryScore']['value']:.4f}")
