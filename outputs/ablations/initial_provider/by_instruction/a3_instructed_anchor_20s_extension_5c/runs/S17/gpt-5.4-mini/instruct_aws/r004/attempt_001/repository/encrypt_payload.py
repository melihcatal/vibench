import boto3

from security_client import get_kms_key_id, load_security_client_config
from security_models import EncryptPayloadRequest, EncryptPayloadResponse, b64encode_bytes, normalize_text


def encrypt_payload(plaintext: str) -> EncryptPayloadResponse:
    config = load_security_client_config()
    kms = boto3.client("kms", region_name=config.region_name)
    request = EncryptPayloadRequest(plaintext=normalize_text(plaintext))
    response = kms.encrypt(KeyId=config.kms_key_id, Plaintext=request.plaintext.encode("utf-8"))
    return EncryptPayloadResponse(ciphertext_blob=b64encode_bytes(response["CiphertextBlob"]), key_id=response["KeyId"])


def main() -> None:
    encrypt_payload("sample plaintext")


if __name__ == "__main__":
    main()
