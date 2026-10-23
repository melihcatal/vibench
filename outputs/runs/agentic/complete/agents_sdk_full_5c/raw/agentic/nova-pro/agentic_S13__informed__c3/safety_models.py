from typing import Dict, Any

def normalize_perspective_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v['score'] for k, v in response['attributeScores'].items()}

def normalize_tisane_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {item['text']: item['scores'] for item in response['results']}