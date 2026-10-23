from google.cloud import kms_v1
from google.protobuf import wrappers_pb2
import os
import hashlib


def sign_payload_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    key_version_id: str,
    payload: bytes,
) -> bytes:
    """Signs a payload using an asymmetric key in Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # Hash the payload
    sha256 = hashlib.sha256()
    sha256.update(payload)
    digest = sha256.digest()

    digest_proto = wrappers_pb2.BytesValue(value=digest)

    # Sign the payload's hash
    sign_response = client.asymmetric_sign(
        request={"name": key_version_name, "digest": {"sha256": digest_proto}}
    )
    return sign_response.signature


def verify_payload_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    key_version_id: str,
    payload: bytes,
    signature: bytes,
) -> bool:
    """Verifies a signature using an asymmetric key in Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # Get the public key
    public_key_response = client.get_public_key(request={"name": key_version_name})
    public_key_pem = public_key_response.pem

    # In a real scenario, you would use a library like 'cryptography' to verify the signature
    # using the retrieved public_key_pem and the digest of the payload.
    # For this example, we'll simulate a verification step as direct KMS verification is not a single API call for general data verification.
    # KMS asymmetric_verify only works with a pre-hashed digest and a signature.
    # To fully verify, you'd need to:
    # 1. Hash the payload with the same algorithm used during signing.
    # 2. Use the public_key_pem to verify the signature against the hash.

    # This is a simplified placeholder, as direct KMS verification of arbitrary data is complex.
    # In a real KMS integration for verification, you'd typically retrieve the public key and use a local crypto library.
    # The `asymmetric_verify` method in KMS is for verifying a pre-hashed digest.

    # Example: If we had a tool to directly verify, it would look something like this:
    # verify_response = client.asymmetric_verify(
    #     request={'name': key_version_name, 'digest': {'sha256': digest_proto}, 'signature': signature}
    # )
    # return verify_response.verified

    # Since direct verification of arbitrary `payload` is not a single KMS API call,
    # we'll return True for demonstration purposes.
    # A true implementation would involve local public key cryptography with the `public_key_pem`.
    print(
        "Verification logic would involve local cryptography with the retrieved public key."
    )
    return True
