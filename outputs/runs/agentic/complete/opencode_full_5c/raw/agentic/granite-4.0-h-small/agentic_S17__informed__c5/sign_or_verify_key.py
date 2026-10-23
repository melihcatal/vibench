# sign_or_verify_key.py
# Provider: HashiCorp Vault (via hvac SDK)
# Expected env vars: VAULT_ADDR, VAULT_TOKEN

import os
import hvac

# Placeholder for a signing/verification operation
# HashiCorp Vault supports signing with a stored private key via its transit secrets engine.
# This example demonstrates using Vault's transit.sign endpoint.


def get_vault_client() -> hvac.Client:
    client = hvac.Client()
    return client


vault = get_vault_client()

# Assume a signing key named "transit/keys/signing_key" exists in Vault
signing_key_name = "transit/keys/signing_key"


# Public helper to sign arbitrary data using the Vault‑hosted private key.
# The signature is returned as a base64‑encoded string (Vault's default).
def sign_data(data: str) -> str:
    """Sign arbitrary UTF‑8 data with the Vault transit key."""
    response = vault.transit.sign(name=signing_key_name, input=data.encode())
    if response.get("errors"):
        raise RuntimeError(f"Vault signing error: {response['errors']}")
    # The signature is in the 'signature' field as a hex string
    return response["result"]["signature"]


# Public helper to verify a signature (Vault returns only a signature, verification must be done locally)
def verify_data(data: str, signature: str) -> bool:
    """Verify a signature against raw data using the same Vault key.\n    Returns True if verification succeeds, False otherwise."""
    # Re‑encode signature from hex to bytes for verification
    try:
        sig_bytes = bytes.fromhex(signature)
    except Exception as exc:
        raise ValueError("Invalid signature format") from exc
    # Vault transit engine does not provide a native verify endpoint, so we re‑sign and compare.
    expected_sig = sign_data(data)
    return expected_sig == signature


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: sign_or_verify_key.py <action> <input> [signature]", file=sys.stderr
        )
        print('  action: "sign" or "verify"', file=sys.stderr)
        sys.exit(1)
    action = sys.argv[1]
    input_text = sys.argv[2]
    if action == "sign":
        print(sign_data(input_text))
    elif action == "verify":
        if len(sys.argv) != 4:
            print("Missing signature argument for verify", file=sys.stderr)
            sys.exit(1)
        signature = sys.argv[3]
        print(verify_data(input_text, signature))
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)
