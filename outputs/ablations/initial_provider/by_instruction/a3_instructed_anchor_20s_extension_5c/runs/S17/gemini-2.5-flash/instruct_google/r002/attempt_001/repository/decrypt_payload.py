import os
from google.cloud import kms_v1
from security_client import KmsClient
from security_models import PlaintextPayload, CiphertextPayload

def decrypt_payload(ciphertext: CiphertextPayload) -> PlaintextPayload:
    kms_client = KmsClient()
    name = kms_client.get_key_path(ciphertext.key_id)

    response = kms_client.client.decrypt(name=name, ciphertext=ciphertext.data)
    
    # Convert the decrypted bytes back to a string
    plaintext_data = response.plaintext.decode("utf-8")
    
    return PlaintextPayload(data=plaintext_data)
