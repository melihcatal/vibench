from typing import Dict, Any



class SecurityRequest:
    def __init__(self, payload: Dict[str, Any], config: Dict[str, Any]):
        self.payload = payload
        self.config = config



class SecurityResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data



def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'plaintext': payload['plaintext'].encode() if 'plaintext' in payload else None,
            'ciphertext': payload['ciphertext'] if 'ciphertext' in payload else None,
            'message': payload['message'].encode() if 'message' in payload else None,
            'signature': payload['signature'] if 'signature' in payload else None}



def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'ciphertext': response['CiphertextBlob'] if 'CiphertextBlob' in response else None,
            'plaintext': response['Plaintext'].decode() if 'Plaintext' in response else None,
            'signature': response['Signature'] if 'Signature' in response else None,
            'is_valid': response['SignatureValid'] if 'SignatureValid' in response else None}
