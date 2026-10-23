from typing import Dict

def normalize_payload(payload: Dict) -> Dict:
    return {
        'text': payload.get('text', ''),
        'ssml': payload.get('ssml', ''),
        'voice': payload.get('voice', 'en-US-JennyNeural')
    }

def parse_response(response):
    return {
        'audio_bytes': response.audio_data,
        'content_type': 'audio/mpeg'
    }