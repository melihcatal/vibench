import os
from typing import Dict
from googleapiclient.discovery import build

perspective_key = os.getenv("PERSPECTIVE_API_KEY")
if not perspective_key:
    raise ValueError("PERSPECTIVE_API_KEY environment variable required")

analyzer = build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=perspective_key,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
)

def check_document_safety(doc: Dict) -> Dict:
    text = " ".join(str(v) for v in doc.values() if isinstance(v, (str, dict)))
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    response = analyzer.comments().analyze(body=analyze_request).execute()
    return response["attributeScores"]