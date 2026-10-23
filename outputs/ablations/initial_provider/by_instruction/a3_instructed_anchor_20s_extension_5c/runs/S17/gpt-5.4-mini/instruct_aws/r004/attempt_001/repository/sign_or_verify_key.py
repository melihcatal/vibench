import boto3

from security_client import get_signing_key_id, load_security_client_config
from security_models import SignOrVerifyRequest, SignOrVerifyResponse, b64encode_bytes, b64decode_text, normalize_text


def sign_or_verify_key(message: str, signature: str | None = None) -> SignOrVerifyResponse:
    config = load_security_client_config()
    kms = boto3.client("kms", region_name=config.region_name)
    key_id = get_signing_key_id()
    request = SignOrVerifyRequest(message=normalize_text(message), signature=signature)
    if request.signature is None:
        result = kms.sign(
            KeyId=key_id,
            Message=request.message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return SignOrVerifyResponse(verified=True, signature=b64encode_bytes(result["Signature"]))
    result = kms.verify(
        KeyId=key_id,
        Message=request.message.encode("utf-8"),
        MessageType="RAW",
        Signature=b64decode_text(request.signature),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return SignOrVerifyResponse(verified=bool(result["SignatureValid"]))


def main() -> None:
    sign_or_verify_key("sample message")


if __name__ == "__main__":
    main()
