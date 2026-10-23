from typing import Dict

def normalize_encrypt_response(response: Dict) -> Dict:
    return {'ciphertext': response['CiphertextBlob']}

def normalize_decrypt_response(response: Dict) -> Dict:
    return {'plaintext': response['Plaintext'].decode('utf-8')}

def normalize_envelope_encrypt_response(response: Dict) -> Dict:
    return {'encrypted_data_key': response['CiphertextBlob'], 'encrypted_payload': response['CiphertextBlob']}

def normalize_sign_response(response: Dict) -> Dict:
    return {'signature': response['Signature']}

def normalize_verify_response(response: Dict) -> Dict:
    return {'verified': response['SignatureValid']}
