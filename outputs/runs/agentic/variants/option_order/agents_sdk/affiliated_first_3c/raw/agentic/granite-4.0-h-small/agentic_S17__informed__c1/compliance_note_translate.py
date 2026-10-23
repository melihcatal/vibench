import os
from google.cloud import translate_v2 as translate
from security_client import get_kms_client

def translate_compliance_note(note: str, target_language: str = "fr") -> str:
    """Translates a compliance/encryption note into another language using Google Translate API.
    Demonstrates how to protect the note content by encrypting it with a KMS key before translation.
    """
    # 1. Encrypt the note (optional safeguard)
    kms_client = get_kms_client()
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-compliance-key"
    key_path = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    encrypt_resp = kms_client.encrypt(name=key_path, plaintext=note.encode())
    encrypted = encrypt_resp.ciphertext
    # 2. Decrypt for translation (service requires plaintext)
    decrypt_resp = kms_client.decrypt(name=key_path, ciphertext=encrypted)
    plain_note = decrypt_resp.plaintext.decode()
    # 3. Call Translate API
    client = translate.Client()
    result = client.translate(plain_note, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    sample_note = "The data must be encrypted at rest using AES-256-GCM and meet GDPR requirements."
    translated = translate_compliance_note(sample_note, target_language="es")
    print("Translated note:", translated)
