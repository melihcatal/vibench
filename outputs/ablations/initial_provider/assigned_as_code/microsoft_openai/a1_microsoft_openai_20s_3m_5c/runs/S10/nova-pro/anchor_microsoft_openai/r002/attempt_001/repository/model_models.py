from typing import Dict, Any


def normalize_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': payload['text']}


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': response['choices'][0]['message']['content']}