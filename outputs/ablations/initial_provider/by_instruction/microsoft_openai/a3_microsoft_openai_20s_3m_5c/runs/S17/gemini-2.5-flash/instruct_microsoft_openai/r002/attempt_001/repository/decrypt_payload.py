import os
import argparse
from security_client import SecurityClient
from security_models import DecryptRequest, DecryptResponse

def decrypt_payload_main():
    parser = argparse.ArgumentParser(description="Decrypt a ciphertext payload using Azure Key Vault.")
    parser.add_argument("--ciphertext", required=True, help="The ciphertext (hex string) to decrypt.")
    parser.add_argument("--key-name", required=True, help="The name of the key in Azure Key Vault.")
    parser.add_argument("--key-vault-url", required=False, 
                        help="The URL of the Azure Key Vault. Defaults to AZURE_KEY_VAULT_URL environment variable.")

    args = parser.parse_args()

    key_vault_url = args.key_vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("Azure Key Vault URL not provided. Please set --key-vault-url or AZURE_KEY_VAULT_URL environment variable.")

    client = SecurityClient()
    request = DecryptRequest(
        ciphertext=args.ciphertext,
        key_name=args.key_name,
        key_vault_url=key_vault_url
    )

    try:
        response: DecryptResponse = client.decrypt_with_key_vault(request)
        print(f"Decryption successful. Plaintext: {response.plaintext}")
    except Exception as e:
        print(f"Decryption failed: {e}")

if __name__ == "__main__":
    decrypt_payload_main()
