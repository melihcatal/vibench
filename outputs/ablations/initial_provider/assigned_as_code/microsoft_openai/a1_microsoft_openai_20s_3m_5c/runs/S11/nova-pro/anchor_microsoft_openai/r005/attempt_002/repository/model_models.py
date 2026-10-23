from typing import Any, Dict

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': payload['text']}

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': response['choices'][0]['message']['content'] or ''}