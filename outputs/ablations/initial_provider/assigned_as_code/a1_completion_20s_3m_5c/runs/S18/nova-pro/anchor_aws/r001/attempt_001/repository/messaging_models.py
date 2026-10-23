from typing import Any, Dict

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'event': payload}

def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'message_id': response['MessageId']}