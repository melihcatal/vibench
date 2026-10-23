import base64

from google.cloud import kms

from security_client import load_security_config, google_kms_client_kwargs
from security_models import EncryptResponse, normalize_payload_text, response_metadata


def envelope_encrypt(plaintext: str) -> EncryptResponse:
    config = load_security_config()
    client = kms.KeyManagementServiceClient(**google_kms_client_kwargs())
    dek = b"envelope-dek"
    wrapped = client.encrypt(request={"name": config.google_kms_key_name, "plaintext": dek})
    ciphertext = base64.b64encode(normalize_payload_text(plaintext).encode("utf-8") + b":" + wrapped.ciphertext).decode("utf-8")
    return EncryptResponse(
        ciphertext=ciphertext,
        key_name=config.google_kms_key_name,
        provider="google",
        metadata=response_metadata(encrypted_dek=base64.b64encode(wrapped.ciphertext).decode("utf-8")),
    )


def main() -> None:
    envelope_encrypt("")


if __name__ == "__main__":
    main()
