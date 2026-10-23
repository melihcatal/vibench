import os
from googleapiclient import discovery

def moderate_batch_messages(messages: list[str]) -> list[dict]:
    API_KEY = os.getenv("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    decisions = []
    for message in messages:
        analyze_request = {
            'comment': {'text': message},
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
        decisions.append({
            "message": message,
            "scores": {
                attr: response['attributeScores'][attr]['summaryScore']['value']
                for attr in analyze_request['requestedAttributes']
            }
        })
    return decisions
