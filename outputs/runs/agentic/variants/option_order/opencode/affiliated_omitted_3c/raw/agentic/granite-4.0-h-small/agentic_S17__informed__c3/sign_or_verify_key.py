import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# HashiCorp Vault integration example
# Requires hvac library and Vault token (VAULT_TOKEN) pointing to a Vault with a signing key
import hvac

# Local helper imports
from security_client import KeyManagementClient
from security_models import PlaintextPayload, SignaturePayload


class VaultSigningClient:
    """Client for signing and verifying data using HashiCorp Vault transit secrets engine."""

    def __init__(self, vault_addr: str, token: str, signing_key_path: str):
        self.client = hvac.Client(url=vault_addr, token=token)
        self.signing_key_path = signing_key_path
        if not self.client.is_authenticated():
            raise RuntimeError("Vault authentication failed")

    def sign(self, data: str) -> SignaturePayload:
        """Sign data using Vault's transit engine with RSA-SHA256."""
        try:
            response = self.client.transit_sign(
                name=self.signing_key_path, input=data, algorithm="rsa-sha256"
            )
            signature = response["signature"]
            return SignaturePayload(signature=signature)
        except hvac.exceptions.VaultError as e:
            raise RuntimeError(f"Vault signing failed: {e}")

    def verify(self, data: str, signature: str) -> bool:
        """Verify a signature produced by Vault."""
        try:
            response = self.client.transit_verify(
                name=self.signing_key_path, input=data, signature=signature
            )
            return response["valid"]
        except hvac.exceptions.VaultError as e:
            raise RuntimeError(f"Vault verification failed: {e}")


# Load configuration from environment
VAULT_ADDR = os.getenv("VAULT_ADDR")
if not VAULT_ADDR:
    raise RuntimeError("Set VAULT_ADDR environment variable before running.")
TOKEN = os.getenv("VAULT_TOKEN")
if not TOKEN:
    raise RuntimeError("Set VAULT_TOKEN environment variable before running.")
SIGNING_KEY_PATH = os.getenv("VAULT_SIGNING_KEY_PATH", "transit/signing-key")

signer = VaultSigningClient(VAULT_ADDR, TOKEN, SIGNING_KEY_PATH)

# Example usage
if __name__ == "__main__":
    message = "Important document content"
    sig_payload = signer.sign(message)
    print("Signature (base64):", sig_payload.signature)
    # Verification
    is_valid = signer.verify(message, sig_payload.signature)
    print("Signature valid?", is_valid)
