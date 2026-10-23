from typing import Dict, Any


def normalize_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": payload["text"],
        "modelId": payload.get("modelId", "us.amazon.nova-pro-v1:0"),
    }


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": ''.join(block['text'] for block in response['output']['message']['content'] if 'text' in block),
        "usage": response['usage'],
        "modelId": response['modelId'],
    }