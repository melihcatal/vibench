from typing import Any, Dict

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'language_code': payload.get('language_code', 'en-US'),
        'sample_rate_hz': payload.get('sample_rate_hz', 16000),
        'audio_chunks': payload.get('audio_chunks', [])
    }

def parse_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'text': result.get('text', ''),
        'is_final': result.get('is_final', False)
    }