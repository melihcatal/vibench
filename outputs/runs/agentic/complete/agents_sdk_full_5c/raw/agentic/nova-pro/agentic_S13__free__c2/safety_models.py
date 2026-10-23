from typing import Dict

def normalize_response(response: Dict) -> Dict:
    return {k: v['summaryScore']['value'] for k, v in response['attributeScores'].items()}