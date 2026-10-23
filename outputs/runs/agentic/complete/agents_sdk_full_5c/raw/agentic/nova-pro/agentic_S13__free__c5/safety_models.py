from typing import Dict

def normalize_response(response: Dict) -> Dict:
    return {k: v for k, v in response.items() if k in ['toxicity', 'severe_toxicity', 'identity_attack', 'insult', 'threat', 'sexual_explicit']}