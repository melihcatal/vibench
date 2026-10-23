from typing import Dict, Any

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': payload.get('text', ''), 'ssml': payload.get('ssml', '')}

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'audio_bytes': response.get('audio_bytes', b''), 'content_type': response.get('content_type', '')}