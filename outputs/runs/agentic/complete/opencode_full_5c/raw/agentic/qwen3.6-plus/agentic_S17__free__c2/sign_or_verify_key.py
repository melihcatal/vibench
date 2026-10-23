import os
import sys
import argparse
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    SigningAlgorithm,
    MessageType,
)
from security_client import (
    execute_sign,
    execute_verify,
    get_kms_client,
    serialize_response_for_api,
)


def sign_message(
    message,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    message_type: MessageType = MessageType.RAW,
    encryption_context: dict = None,
) -> SignResponse:
    request = SignRequest(
        key_id=key_id,
        message=message,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
        encryption_context=encryption_context,
    )
    client = get_kms_client()
    response = execute_sign(request, client=client)
    return response


def verify_signature(
    message,
    signature,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256,
    message_type: MessageType = MessageType.RAW,
    encryption_context: dict = None,
) -> VerifyResponse:
    request = VerifyRequest(
        key_id=key_id,
        message=message,
        signature=signature,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
        encryption_context=encryption_context,
    )
    client = get_kms_client()
    response = execute_verify(request, client=client)
    return response


def main():
    parser = argparse.ArgumentParser(description="Sign or verify using AWS KMS")
    parser.add_argument("action", choices=["sign", "verify"], help="Action to perform")
    parser.add_argument(
        "--key-id", default=os.environ.get("AWS_KMS_KEY_ID"), help="KMS Key ID"
    )
    parser.add_argument(
        "--algorithm", default="ECDSA_SHA_256", help="Signing algorithm"
    )
    parser.add_argument("--signature-file", help="Path to signature file (for verify)")
    parser.add_argument("--output-file", help="Path to output file (for sign)")
    args = parser.parse_args()
    if not args.key_id:
        print("Error: --key-id or AWS_KMS_KEY_ID is required", file=sys.stderr)
        sys.exit(1)
    message = sys.stdin.buffer.read()
    if not message:
        print("Error: No message provided on stdin", file=sys.stderr)
        sys.exit(1)
    algorithm = SigningAlgorithm[args.algorithm]
    encryption_context = None
    ctx_file = os.environ.get("ENCRYPTION_CONTEXT_FILE")
    if ctx_file and os.path.exists(ctx_file):
        import json

        with open(ctx_file) as f:
            encryption_context = json.load(f)
    if args.action == "sign":
        response = sign_message(
            message, args.key_id, algorithm, encryption_context=encryption_context
        )
        output = serialize_response_for_api(response)
        import json

        if args.output_file:
            with open(args.output_file, "wb") as f:
                f.write(response.signature)
        print(json.dumps(output, indent=2))
    elif args.action == "verify":
        if not args.signature_file:
            print("Error: --signature-file is required for verify", file=sys.stderr)
            sys.exit(1)
        with open(args.signature_file, "rb") as f:
            signature = f.read()
        response = verify_signature(
            message,
            signature,
            args.key_id,
            algorithm,
            encryption_context=encryption_context,
        )
        output = serialize_response_for_api(response)
        import json

        print(json.dumps(output, indent=2))
        sys.exit(0 if response.signature_valid else 1)


if __name__ == "__main__":
    main()
