import base64

from google.cloud import kms

from security_client import load_security_config, google_kms_client_kwargs
from security_models import EncryptRequest, EncryptResponse, normalize_payload_text, response_metadata


def encrypt_payload(plaintext: str) -> EncryptResponse:
    config = load_security_config()
    client = kms.KeyManagementServiceClient(**google_kms_client_kwargs())
    request = EncryptRequest(plaintext=normalize_payload_text(plaintext), key_name=config.google_kms_key_name)
    response = client.encrypt(request={"name": request.key_name, "plaintext": request.plaintext.encode("utf-8")})
    ciphertext = base64.b64encode(response.ciphertext).decode("utf-8")
    return EncryptResponse(
        ciphertext=ciphertext,
        key_name=request.key_name,
        provider="google",
        metadata=response_metadata(name=response.name),
    )


def main() -> None:
    encrypt_payload("")


if __name__ == "__main__":
    main()
