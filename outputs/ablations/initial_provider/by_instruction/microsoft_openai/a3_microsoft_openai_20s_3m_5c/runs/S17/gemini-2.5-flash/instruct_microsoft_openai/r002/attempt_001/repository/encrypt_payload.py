import os
import argparse
from security_client import SecurityClient
from security_models import EncryptRequest, EncryptResponse

def encrypt_payload_main():
    parser = argparse.ArgumentParser(description="Encrypt a plaintext payload using Azure Key Vault.")
    parser.add_argument("--plaintext", required=True, help="The plaintext string to encrypt.")
    parser.add_argument("--key-name", required=True, help="The name of the key in Azure Key Vault.")
    parser.add_argument("--key-vault-url", required=False, 
                        help="The URL of the Azure Key Vault. Defaults to AZURE_KEY_VAULT_URL environment variable.")

    args = parser.parse_args()

    key_vault_url = args.key_vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("Azure Key Vault URL not provided. Please set --key-vault-url or AZURE_KEY_VAULT_URL environment variable.")

    client = SecurityClient()
    request = EncryptRequest(
        plaintext=args.plaintext,
        key_name=args.key_name,
        key_vault_url=key_vault_url
    )

    try:
        response: EncryptResponse = client.encrypt_with_key_vault(request)
        print(f"Encryption successful. Key ID: {response.key_id}")
        print(f"Ciphertext (hex): {response.ciphertext}")
    except Exception as e:
        print(f"Encryption failed: {e}")

if __name__ == "__main__":
    encrypt_payload_main()
