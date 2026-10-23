from typing import Any, Dict, Union

def create_request(text: str, voice: str, prosody: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'text': text,
        'voice': voice,
        'prosody': prosody
    }

def parse_response(response: Dict[str, Any]) -> Union[str, bytes]:
    if 'audioContent' in response:
        return response['audioContent']
    elif 'text' in response:
        return response['text']
    else:
        raise ValueError('Invalid response format')

def normalize_prosody(prosody: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in prosody.items():
        if isinstance(value, str):
            normalized[key] = value.lower()
        elif isinstance(value, (int, float)):
            normalized[key] = round(value, 2)
    return normalized