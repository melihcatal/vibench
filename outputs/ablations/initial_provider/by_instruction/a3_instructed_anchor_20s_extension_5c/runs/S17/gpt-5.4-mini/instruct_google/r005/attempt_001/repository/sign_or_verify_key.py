import base64

from google.cloud import kms

from security_client import load_security_config, google_kms_client_kwargs
from security_models import SignRequest, SignResponse, VerifyResponse, normalize_payload_text, response_metadata


def sign_or_verify_key(payload: str, signature: str = ""):
    config = load_security_config()
    client = kms.KeyManagementServiceClient(**google_kms_client_kwargs())
    request = SignRequest(payload=normalize_payload_text(payload), key_name=config.google_kms_key_name)
    digest = {"sha256": request.payload.encode("utf-8")[:32]}
    if signature:
        verified = base64.b64encode(digest["sha256"]).decode("utf-8") == normalize_payload_text(signature)
        return VerifyResponse(verified=verified, key_name=request.key_name, provider="google", metadata=response_metadata())
    response = client.asymmetric_sign(request={"name": request.key_name, "digest": digest})
    return SignResponse(
        signature=base64.b64encode(response.signature).decode("utf-8"),
        key_name=request.key_name,
        provider="google",
        metadata=response_metadata(name=response.name),
    )


def main() -> None:
    sign_or_verify_key("")


if __name__ == "__main__":
    main()
