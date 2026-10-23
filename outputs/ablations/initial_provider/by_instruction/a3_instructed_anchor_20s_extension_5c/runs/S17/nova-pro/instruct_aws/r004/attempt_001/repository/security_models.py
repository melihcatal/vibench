from typing import Dict, Any

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'CiphertextBlob': response.get('CiphertextBlob', b''),
        'Plaintext': response.get('Plaintext', b''),
        'KeyId': response.get('KeyId', '')
    }