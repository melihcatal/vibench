from security_client import create_kms_client, get_kms_key_id, b64_to_bytes
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(ciphertext_blob, key_id=None):
    request = DecryptRequest.from_payload({"ciphertext_blob": ciphertext_blob, "key_id": key_id or get_kms_key_id()})
    kms = create_kms_client()
    kwargs = {"CiphertextBlob": request.ciphertext_blob}
    if request.key_id:
        kwargs["KeyId"] = request.key_id
    result = kms.decrypt(**kwargs)
    plaintext = result["Plaintext"].decode("utf-8")
    return DecryptResponse(plaintext=plaintext, key_id=result.get("KeyId", request.key_id or "")).to_payload()
