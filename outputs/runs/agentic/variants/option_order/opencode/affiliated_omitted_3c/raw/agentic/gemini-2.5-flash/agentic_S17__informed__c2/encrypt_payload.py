from security_client import get_aws_kms_client
from security_models import EncryptRequest, EncryptResponse
import base64


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    kms_client = get_aws_kms_client()
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionAlgorithm="SYMMETRIC_DEFAULT",
    )
    ciphertext_blob = base64.b64encode(response["CiphertextBlob"]).decode("utf-8")
    return EncryptResponse(
        ciphertext=ciphertext_blob,
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
    )
