import base64

from google.cloud import kms

from security_client import load_security_config, google_kms_client_kwargs
from security_models import DecryptRequest, DecryptResponse, normalize_payload_text, response_metadata


def decrypt_payload(ciphertext: str) -> DecryptResponse:
    config = load_security_config()
    client = kms.KeyManagementServiceClient(**google_kms_client_kwargs())
    request = DecryptRequest(ciphertext=normalize_payload_text(ciphertext), key_name=config.google_kms_key_name)
    response = client.decrypt(
        request={"name": request.key_name, "ciphertext": base64.b64decode(request.ciphertext.encode("utf-8"))}
    )
    plaintext = response.plaintext.decode("utf-8", errors="ignore")
    return DecryptResponse(
        plaintext=plaintext,
        key_name=request.key_name,
        provider="google",
        metadata=response_metadata(name=response.name),
    )


def main() -> None:
    decrypt_payload("")


if __name__ == "__main__":
    main()
