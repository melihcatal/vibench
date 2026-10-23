import os
import argparse
from security_client import SecurityClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse

def envelope_encrypt_main():
    parser = argparse.ArgumentParser(description="Perform envelope encryption using Azure Key Vault.")
    parser.add_argument("--plaintext", required=True, help="The plaintext string to encrypt.")
    parser.add_argument("--key-name", required=True, help="The name of the key in Azure Key Vault (for wrapping the CEK).")
    parser.add_argument("--key-vault-url", required=False, 
                        help="The URL of the Azure Key Vault. Defaults to AZURE_KEY_VAULT_URL environment variable.")
    parser.add_argument("--algorithm", default="RSA_OAEP", help="The algorithm to use for key wrapping (e.g., RSA_OAEP).")

    args = parser.parse_args()

    key_vault_url = args.key_vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("Azure Key Vault URL not provided. Please set --key-vault-url or AZURE_KEY_VAULT_URL environment variable.")

    client = SecurityClient()
    request = EnvelopeEncryptRequest(
        plaintext=args.plaintext,
        key_name=args.key_name,
        key_vault_url=key_vault_url,
        algorithm=args.algorithm
    )

    try:
        response: EnvelopeEncryptResponse = client.envelope_encrypt_with_key_vault(request)
        print(f"Envelope encryption successful. Key ID: {response.key_id}")
        print(f"Encrypted CEK (hex): {response.encrypted_key}")
        print(f"Ciphertext (data, placeholder): {response.ciphertext}")
    except Exception as e:
        print(f"Envelope encryption failed: {e}")

if __name__ == "__main__":
    envelope_encrypt_main()
