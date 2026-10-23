from typing import Dict, Any

def create_payload(text: str) -> Dict[str, Any]:
    return {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }

def parse_response(response: Dict[str, Any]) -> float:
    return response['attributeScores']['TOXICITY']['summaryScore']['value']