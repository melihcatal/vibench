import boto3

from security_client import load_security_client_config
from security_models import DecryptPayloadRequest, DecryptPayloadResponse, b64decode_text, normalize_text


def decrypt_payload(ciphertext_blob: str) -> DecryptPayloadResponse:
    config = load_security_client_config()
    kms = boto3.client("kms", region_name=config.region_name)
    request = DecryptPayloadRequest(ciphertext_blob=normalize_text(ciphertext_blob))
    response = kms.decrypt(CiphertextBlob=b64decode_text(request.ciphertext_blob))
    return DecryptPayloadResponse(plaintext=response["Plaintext"].decode("utf-8"))


def main() -> None:
    decrypt_payload("")


if __name__ == "__main__":
    main()
