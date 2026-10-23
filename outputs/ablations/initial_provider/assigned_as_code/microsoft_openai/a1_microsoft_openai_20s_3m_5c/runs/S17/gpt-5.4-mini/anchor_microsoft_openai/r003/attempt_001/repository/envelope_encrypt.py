from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm, SignatureAlgorithm

from security_models import build_envelope_payload


def envelope_encrypt(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            cek_response = client.encrypt(EncryptionAlgorithm.rsa_oaep_256, payload['content_key'])
            wrapped_key = cek_response.ciphertext
            iv = payload.get('iv') or b''
            content = payload['plaintext']
            signature = client.sign(SignatureAlgorithm.rs256, content).signature
    return build_envelope_payload(content, wrapped_key, iv, signature, config['key_id'])
