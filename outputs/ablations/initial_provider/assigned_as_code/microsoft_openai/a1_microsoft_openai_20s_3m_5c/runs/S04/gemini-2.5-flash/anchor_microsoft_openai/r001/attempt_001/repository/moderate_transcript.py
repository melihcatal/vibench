import os
from googleapiclient import discovery
from speech_models import ModerationPayload

def moderate_transcript(payload: ModerationPayload):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        static_discovery=False
    )

    if not os.environ.get("PERSPECTIVE_API_KEY"):
        raise ValueError("Perspective API key not found. Please set PERSPECTIVE_API_KEY environment variable.")

    analyze_request = {
        'comment': { 'text': payload.text },
        'requestedAttributes': { 'TOXICITY': {} }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    
    return {"toxicity_score": toxicity_score}
