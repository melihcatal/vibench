import base64
import binascii
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Optional
from urllib import error, request


AWS_KMS_HOST = "kms.us-east-1.amazonaws.com"


@dataclass
class SignOrVerifyResult:
    algorithm: str
    key_id: str
    message_digest_b64: str
    signature_b64: Optional[str]
    verified: Optional[bool]
    provider: str = "aws-kms"


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _kms_request(action: str, payload: dict[str, Any], region: Optional[str] = None) -> dict[str, Any]:
    region = region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    host = f"kms.{region}.amazonaws.com"
    req = request.Request(
        f"https://{host}/",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": f"TrentService.{action}",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"AWS KMS {action} failed: {exc.code} {body}") from exc


def sign_payload(key_id: str, message: bytes, region: Optional[str] = None) -> SignOrVerifyResult:
    digest = _sha256(message)
    response = _kms_request(
        "Sign",
        {
            "KeyId": key_id,
            "Message": _b64encode(digest),
            "MessageType": "DIGEST",
            "SigningAlgorithm": "RSASSA_PSS_SHA_256",
        },
        region=region,
    )
    return SignOrVerifyResult(
        algorithm=response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
        key_id=response.get("KeyId", key_id),
        message_digest_b64=_b64encode(digest),
        signature_b64=_b64encode(_b64decode(response["Signature"])),
        verified=None,
    )


def verify_payload(key_id: str, message: bytes, signature_b64: str, region: Optional[str] = None) -> SignOrVerifyResult:
    digest = _sha256(message)
    response = _kms_request(
        "Verify",
        {
            "KeyId": key_id,
            "Message": _b64encode(digest),
            "MessageType": "DIGEST",
            "Signature": signature_b64,
            "SigningAlgorithm": "RSASSA_PSS_SHA_256",
        },
        region=region,
    )
    return SignOrVerifyResult(
        algorithm=response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
        key_id=response.get("KeyId", key_id),
        message_digest_b64=_b64encode(digest),
        signature_b64=signature_b64,
        verified=bool(response.get("SignatureValid", False)),
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--verify-signature", default=None)
    parser.add_argument("--region", default=None)
    args = parser.parse_args()

    message = args.message.encode("utf-8")
    if args.verify_signature:
        result = verify_payload(args.key_id, message, args.verify_signature, region=args.region)
    else:
        result = sign_payload(args.key_id, message, region=args.region)
    print(json.dumps(result.__dict__, sort_keys=True))


if __name__ == "__main__":
    main()
