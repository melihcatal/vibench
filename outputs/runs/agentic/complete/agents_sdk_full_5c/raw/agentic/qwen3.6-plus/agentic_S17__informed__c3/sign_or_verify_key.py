"""
[SAME-SCENARIO] sign_or_verify_key.py - Uses a managed key service for signing or verification where supported.

Provider: AWS Key Management Service (AWS KMS)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import sys
from typing import Optional, Tuple

from security_client import KMSClientHelper
from security_models import (
    SignRequest,
    SignResponse,
    SigningAlgorithm,
    VerifyRequest,
    VerifyResponse,
    decode_base64_to_bytes,
    encode_bytes_to_base64,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")


def sign_message(
    key_id: str,
    message: bytes,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
    use_digest: bool = False,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> SignResponse:
    """
    Sign a message using an AWS KMS asymmetric signing key.

    Provider: AWS KMS (boto3) via security_client.KMSClientHelper
    Requires an asymmetric KMS key with a signing key usage.
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    if use_digest:
        digest = hashlib.sha256(message).digest()
        request = SignRequest(
            key_id=key_id,
            message=digest,
            signing_algorithm=signing_algorithm,
            message_type="DIGEST",
        )
    else:
        request = SignRequest(
            key_id=key_id,
            message=message,
            signing_algorithm=signing_algorithm,
            message_type="RAW",
        )

    response = client.sign(request)
    logger.info(
        "Message signed with KMS key %s using %s",
        response.key_id,
        response.signing_algorithm,
    )
    return response


def verify_signature(
    key_id: str,
    message: bytes,
    signature: bytes,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
    use_digest: bool = False,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> VerifyResponse:
    """
    Verify a signature using an AWS KMS asymmetric signing key.

    Provider: AWS KMS (boto3) via security_client.KMSClientHelper
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    if use_digest:
        digest = hashlib.sha256(message).digest()
        request = VerifyRequest(
            key_id=key_id,
            message=digest,
            signature=signature,
            signing_algorithm=signing_algorithm,
            message_type="DIGEST",
        )
    else:
        request = VerifyRequest(
            key_id=key_id,
            message=message,
            signature=signature,
            signing_algorithm=signing_algorithm,
            message_type="RAW",
        )

    response = client.verify(request)
    logger.info(
        "Signature verification for KMS key %s: %s",
        response.key_id,
        response.signature_valid,
    )
    return response


def sign_or_verify(
    action: str,
    key_id: str,
    message: bytes,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
    signature: Optional[bytes] = None,
    use_digest: bool = False,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
):
    """
    Unified entry point for signing or verification using AWS KMS.
    """
    if action == "sign":
        return sign_message(
            key_id=key_id,
            message=message,
            signing_algorithm=signing_algorithm,
            use_digest=use_digest,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )
    elif action == "verify":
        if signature is None:
            raise ValueError("Signature is required for verify action")
        return verify_signature(
            key_id=key_id,
            message=message,
            signature=signature,
            signing_algorithm=signing_algorithm,
            use_digest=use_digest,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )
    else:
        raise ValueError(f"Unknown action: {action}. Use 'sign' or 'verify'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sign or verify using AWS KMS asymmetric key"
    )
    parser.add_argument(
        "action",
        choices=["sign", "verify"],
        help="Action to perform",
    )
    parser.add_argument(
        "--key-id",
        required=True,
        help="KMS key ID or ARN for asymmetric signing key",
    )
    parser.add_argument(
        "--message",
        help="Message string to sign or verify",
    )
    parser.add_argument(
        "--message-file",
        help="Path to file containing message",
    )
    parser.add_argument(
        "--signature",
        help="Base64-encoded signature (for verify action)",
    )
    parser.add_argument(
        "--signature-file",
        help="Path to file containing base64-encoded signature (for verify)",
    )
    parser.add_argument(
        "--algorithm",
        default="RSASSA_PKCS1_V1_5_SHA_256",
        choices=[
            "RSASSA_PKCS1_V1_5_SHA_256",
            "RSASSA_PSS_SHA_256",
            "ECDSA_SHA_256",
        ],
        help="Signing algorithm",
    )
    parser.add_argument(
        "--use-digest",
        action="store_true",
        help="Hash the message with SHA-256 before signing/verifying",
    )
    parser.add_argument("--region", help="AWS region for KMS")
    args = parser.parse_args()

    if args.message_file:
        with open(args.message_file, "rb") as f:
            message = f.read()
    elif args.message:
        message = args.message.encode("utf-8")
    else:
        parser.error("--message or --message-file is required")

    signing_algorithm = SigningAlgorithm(args.algorithm)
    sig_bytes: Optional[bytes] = None

    if args.action == "verify":
        if args.signature_file:
            with open(args.signature_file, "r") as f:
                sig_bytes = decode_base64_to_bytes(f.read().strip())
        elif args.signature:
            sig_bytes = decode_base64_to_bytes(args.signature)
        else:
            parser.error("--signature or --signature-file required for verify")

    result = sign_or_verify(
        action=args.action,
        key_id=args.key_id,
        message=message,
        signing_algorithm=signing_algorithm,
        signature=sig_bytes,
        use_digest=args.use_digest,
        region_name=args.region,
    )

    if args.action == "sign":
        assert isinstance(result, SignResponse)
        print(f"KeyId: {result.key_id}")
        print(f"SigningAlgorithm: {result.signing_algorithm}")
        print(f"Signature (base64): {encode_bytes_to_base64(result.signature)}")
    elif args.action == "verify":
        assert isinstance(result, VerifyResponse)
        print(f"KeyId: {result.key_id}")
        print(f"SignatureValid: {result.signature_valid}")


if __name__ == "__main__":
    main()
