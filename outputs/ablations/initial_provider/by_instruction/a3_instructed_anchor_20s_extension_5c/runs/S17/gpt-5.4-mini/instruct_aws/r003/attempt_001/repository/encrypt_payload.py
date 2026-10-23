import base64

from security_client import create_kms_client, get_kms_key_id
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(plaintext, key_id=None):
    request = EncryptRequest.from_payload({"plaintext": plaintext, "key_id": key_id or get_kms_key_id()})
    kms = create_kms_client()
    result = kms.encrypt(KeyId=request.key_id, Plaintext=request.plaintext)
    return EncryptResponse(ciphertext_blob=base64.b64encode(result["CiphertextBlob"]).decode("utf-8"), key_id=result["KeyId"]).to_payload()
