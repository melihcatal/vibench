from typing import Any, Dict, List

def create_request(text: str, voice: str, speed: float) -> Dict[str, Any]:
    return {
        'input': {
            'text': text
        },
        'voice': {
            'name': voice
        },
        'prosody': {
            'rate': speed
        }
    }

def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'audio_content': response.get('audioContent', ''),
        'status': response.get('status', {})
    }

def normalize_text(text: str) -> str:
    # Simple normalization: remove extra spaces and convert to lowercase
    return ' '.join(text.lower().split())
