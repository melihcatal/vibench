from typing import List, Dict
from googleapiclient import discovery
from safety_client import safety_clients_config
from safety_models import ModerationBatchInput

def moderate_batch(input_data: ModerationBatchInput) -> List[Dict]:
    """
    Moderates a batch of user messages using Google's Perspective API.
    """
    api_key = safety_clients_config.PERSPECTIVE_API_KEY
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY (as GOOGLE_API_KEY) is not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    results = []
    for text in input_data.texts:
        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {}
            },
             'doNotStore': True
        }
        
        try:
            response = client.comments().analyze(body=analyze_request).execute()
            scores = {
                attr: response['attributeScores'][attr]['summaryScore']['value']
                for attr in response['attributeScores']
            }
            results.append({
                'text': text,
                'scores': scores,
                'flagged': any(score > 0.7 for score in scores.values())
            })
        except Exception as e:
            results.append({
                'text': text,
                'scores': {},
                'flagged': True,
                'error': str(e)
            })
    
    return results
