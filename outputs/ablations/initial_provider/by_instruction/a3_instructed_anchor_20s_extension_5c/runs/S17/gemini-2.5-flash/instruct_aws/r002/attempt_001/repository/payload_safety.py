import os
from googleapiclient import discovery

def check_payload_safety(text_payload: str) -> dict:
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': { 'text': text_payload },
        'requestedAttributes': { 'TOXICITY': {} }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
