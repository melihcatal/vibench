from typing import List
from safety_client import perspective_client
from safety_models import SafetyResult, normalize_perspective

def moderate_batch(texts: List[str]) -> List[SafetyResult]:
    client = perspective_client()
    results = []
    for text in texts:
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
        raw_response = client.comments().analyze(body=analyze_request).execute()
        results.append(normalize_perspective(raw_response, text))
    return results