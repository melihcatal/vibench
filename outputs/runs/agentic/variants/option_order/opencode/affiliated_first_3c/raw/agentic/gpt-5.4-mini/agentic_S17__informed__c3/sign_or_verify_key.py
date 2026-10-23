import os

from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_client import get_managed_key
from security_models import CryptoResponse, b64e, b64d, normalize_text


def sign_or_verify_key(
    message: str, key_name: str, signature: str = "", verify: bool = False
) -> CryptoResponse:
    key = get_managed_key(key_name)
    client = CryptographyClient(key, key.client)
    msg = normalize_text(message).encode("utf-8")
    if verify:
        result = client.verify(SignatureAlgorithm.rs256, msg, b64d(signature))
        return CryptoResponse(
            key_id=key.id,
            metadata={"provider": "azure-key-vault-keys", "verified": result.is_valid},
        )
    signed = client.sign(SignatureAlgorithm.rs256, msg)
    return CryptoResponse(
        key_id=key.id,
        signature=b64e(signed.signature),
        metadata={"provider": "azure-key-vault-keys"},
    )


if __name__ == "__main__":
    sign_or_verify_key(
        os.environ.get("MESSAGE", ""),
        os.environ.get("KEY_NAME", ""),
        os.environ.get("SIGNATURE", ""),
        os.environ.get("VERIFY", "") == "1",
    )
