from security_client import get_aws_kms_client
from security_models import DecryptRequest, DecryptResponse
import base64


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    kms_client = get_aws_kms_client()
    ciphertext_blob = base64.b64decode(request.ciphertext.encode("utf-8"))
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=request.key_id,
        EncryptionAlgorithm="SYMMETRIC_DEFAULT",
    )
    plaintext = response["Plaintext"].decode("utf-8")
    return DecryptResponse(
        plaintext=plaintext,
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
    )
