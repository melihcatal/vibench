from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'inputText': payload['text'],
        'textGenerationConfig': {
            'maxTokenCount': payload.get('max_token_count', 4096),
            'temperature': payload.get('temperature', 0),
            'topP': payload.get('top_p', 0.9)
        }
    }


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'outputText': response['results'][0]['outputText']}

