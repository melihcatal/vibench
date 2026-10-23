import os
from googleapiclient import discovery

def check_unsafe_content(text, threshold=0.8):
    # Google's Perspective API is used for content moderation.
    api_key = os.getenv("PERSPECTIVE_API_KEY")

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
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

    if toxicity_score > threshold:
        return True, response
    else:
        return False, response
