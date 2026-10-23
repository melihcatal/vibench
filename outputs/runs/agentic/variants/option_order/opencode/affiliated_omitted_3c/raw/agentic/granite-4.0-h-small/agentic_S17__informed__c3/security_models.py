from typing import TypedDict, Final


# Plaintext modeling
class PlaintextPayload(TypedDict):
    plaintext: str


class CiphertextPayload(TypedDict):
    ciphertext: str  # base64 encoded bytes
    key_id: str  # opaque identifier (e.g., AWS KMS data key ID or Vault key path)


# Signature modeling
class SignaturePayload(TypedDict):
    signature: str  # base64 encoded signature bytes


# Enum-like constants for supported providers (used throughout)
PROVIDER_AWS: Final = "aws"
PROVIDER_AZURE: Final = "azure"
PROVIDER_GCP: Final = "gcp"
PROVIDER_ALIBABA: Final = "alibaba"
PROVIDER_HASHICORP_VAULT: Final = "vault"

# Normalizer for incoming plaintext before encryption
NORMALIZED_PLAINTEXT_CHARSET: Final = "utf-8"
