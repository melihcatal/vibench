import os

from security_client import get_transit, load_security_settings
from security_models import (
    CryptoResult,
    build_metadata,
    normalize_key_name,
    normalize_text,
)


def sign_or_verify_key(
    message: str, key_name: str, signature: str = ""
) -> CryptoResult:
    transit = get_transit()
    key = normalize_key_name(key_name)
    msg = normalize_text(message)
    if signature:
        response = transit.verify_data(
            name=key, input=msg, signature=normalize_text(signature)
        )
        ok = bool(response["data"].get("valid", False))
        return CryptoResult(
            ok=ok,
            provider=load_security_settings()["provider"],
            key_name=key,
            payload={"valid": ok, "message": msg, "signature": signature},
            error=None if ok else "invalid signature",
        )
    response = transit.sign_data(name=key, input=msg)
    return CryptoResult(
        ok=True,
        provider=load_security_settings()["provider"],
        key_name=key,
        payload={"signature": response["data"]["signature"], "message": msg},
        error=None,
    )


def main() -> None:
    message = os.getenv("MESSAGE", "")
    key_name = os.getenv("KEY_NAME", "transit-signing-key")
    signature = os.getenv("SIGNATURE", "")
    result = sign_or_verify_key(message, key_name, signature)
    print(result.payload)


if __name__ == "__main__":
    main()
