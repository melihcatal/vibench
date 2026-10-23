# General Text Translation request/response helpers

import logging
from typing import Any, Dict, List

log = logging.getLogger(__name__)

NORMALIZATIONS = {
    'normalize_whitespace': lambda txt: ' '.join(txt.split()),
}

def normalize_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Apply optional normalizations to a translation request payload."""
    if payload.get('normalize_whitespace'):
        payload['text'] = NORMALIZATIONS['normalize_whitespace'](payload['text'])
    return payload

def denormalize_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    """Post-process API response for easier consumption."""
    return {
        'translatedText': resp.get('translatedText', ''),
        'detectedSourceLanguage': resp.get('detectedSourceLanguage', None),
    }

# Provider-specific example: Google Cloud Translation constants (if needed)
# SOURCE_LANGUAGES = ['en', 'es', 'de', ...]
# TARGET_LANGUAGES = ['en', 'es', 'de', ...]
