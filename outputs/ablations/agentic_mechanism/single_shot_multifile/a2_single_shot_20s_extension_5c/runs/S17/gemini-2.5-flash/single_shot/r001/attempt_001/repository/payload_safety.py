from security_client import SecurityClients
from typing import Dict, Any

class SafetyScanResult:
    def __init__(self, text: str, flagged: bool, categories: Dict[str, bool], category_scores: Dict[str, float]):
        self.text = text
        self.flagged = flagged
        self.categories = categories
        self.category_scores = category_scores

def check_payload_safety_openai(payload_text: str) -> SafetyScanResult:
    openai_client = SecurityClients.get_openai_client()
    
    response = openai_client.Moderation.create(
        input=payload_text
    )
    
    first_result = response['results'][0]
    
    return SafetyScanResult(
        text=payload_text,
        flagged=first_result['flagged'],
        categories=first_result['categories'],
        category_scores=first_result['category_scores']
    )