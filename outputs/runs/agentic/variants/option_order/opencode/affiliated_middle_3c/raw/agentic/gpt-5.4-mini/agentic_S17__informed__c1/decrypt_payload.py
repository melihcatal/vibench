import base64
from security_client import get_kms_client, get_region_name
from security_models import DecryptionRequest, DecryptionResponse, normalize_ciphertext_blob, normalize_plaintext

def decrypt_payload(ciphertext_b64: str, region_name: str | None = None) -> DecryptionResponse:
    request = DecryptionRequest(ciphertext_blob=normalize_ciphertext_blob(base64.b64decode(ciphertext_b64)))
    client = get_kms_client(region_name=region_name or get_region_name())
    response = client.decrypt(CiphertextBlob=request.ciphertext_blob)
    return DecryptionResponse(plaintext=normalize_plaintext(response['Plaintext'].decode('utf-8')), provider='aws_kms')
