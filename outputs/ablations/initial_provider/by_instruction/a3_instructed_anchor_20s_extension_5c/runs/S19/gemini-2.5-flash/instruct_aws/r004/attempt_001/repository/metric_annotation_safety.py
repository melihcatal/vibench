import googleapiclient.discovery
from typing import Dict, Any

class SafetyCheckResult:
    def __init__(self, text: str, attributes: Dict[str, Any], is_unsafe: bool):
        self.text = text
        self.attributes = attributes
        self.is_unsafe = is_unsafe

    def to_dict(self):
        return {
            "text": self.text,
            "attributes": self.attributes,
            "is_unsafe": self.is_unsafe
        }

def check_annotation_safety(text: str, client_api_key: str) -> SafetyCheckResult:
    
    # Discovery API is used here because there isn't a direct Python client library
    # for Perspective API in the same way there is for other Google Cloud services.
    # The official client typically recommends using the "commentanalyzer" service.
    
    # The client for the Perspective API.
    # API discovery url: https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1
    service = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=client_api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        cache_discovery=False
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

    response = service.comments().analyze(body=analyze_request).execute()

    is_unsafe = False
    attributes_scores = {}
    for attribute, data in response.get('attributeScores', {}).items():
        score = data['summaryScore']['value']
        attributes_scores[attribute] = score
        # A simple threshold for "unsafe" - adjust as needed
        if score > 0.7:
            is_unsafe = True

    return SafetyCheckResult(text=text, attributes=attributes_scores, is_unsafe=is_unsafe)