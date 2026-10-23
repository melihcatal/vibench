import os
import argparse
import hashlib
from security_client import SecurityClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_or_verify_key_main():
    parser = argparse.ArgumentParser(description="Sign a digest or verify a signature using Azure Key Vault.")
    parser.add_argument("--operation", choices=["sign", "verify"], required=True, help="Operation to perform: 'sign' or 'verify'.")
    parser.add_argument("--input-text", help="The input text to hash and sign/verify (for 'sign' operation). Required for 'sign'.")
    parser.add_argument("--digest", help="The hex-encoded digest to sign or verify. If input-text is provided, digest is computed from it.")
    parser.add_argument("--signature", help="The hex-encoded signature to verify (for 'verify' operation). Required for 'verify'.")
    parser.add_argument("--key-name", required=True, help="The name of the key in Azure Key Vault.")
    parser.add_argument("--key-vault-url", required=False, 
                        help="The URL of the Azure Key Vault. Defaults to AZURE_KEY_VAULT_URL environment variable.")
    parser.add_argument("--algorithm", default="RS256", help="The signing algorithm (e.g., RS256, RS384, RS512).")

    args = parser.parse_args()

    key_vault_url = args.key_vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("Azure Key Vault URL not provided. Please set --key-vault-url or AZURE_KEY_VAULT_URL environment variable.")

    client = SecurityClient()

    digest_to_use = args.digest
    if args.input_text:
        # Compute SHA256 digest of the input text
        digest_to_use = hashlib.sha256(args.input_text.encode('utf-8')).hexdigest()
        print(f"Computed digest from input text: {digest_to_use}")

    if not digest_to_use:
        raise ValueError("Digest or input-text is required for signing/verification.")

    if args.operation == "sign":
        request = SignRequest(
            digest=digest_to_use,
            key_name=args.key_name,
            key_vault_url=key_vault_url,
            algorithm=args.algorithm
        )
        try:
            response: SignResponse = client.sign_with_key_vault(request)
            print(f"Signing successful. Key ID: {response.key_id}")
            print(f"Signature (hex): {response.signature}")
        except Exception as e:
            print(f"Signing failed: {e}")
    elif args.operation == "verify":
        if not args.signature:
            raise ValueError("Signature is required for 'verify' operation.")
        request = VerifyRequest(
            digest=digest_to_use,
            signature=args.signature,
            key_name=args.key_name,
            key_vault_url=key_vault_url,
            algorithm=args.algorithm
        )
        try:
            response: VerifyResponse = client.verify_with_key_vault(request)
            print(f"Verification result: {response.is_valid}")
        except Exception as e:
            print(f"Verification failed: {e}")

if __name__ == "__main__":
    sign_or_verify_key_main()
