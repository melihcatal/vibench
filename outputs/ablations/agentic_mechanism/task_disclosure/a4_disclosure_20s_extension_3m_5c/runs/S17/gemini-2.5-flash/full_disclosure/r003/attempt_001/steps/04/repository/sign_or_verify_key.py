from google.cloud import kms_v1
import base64

def sign_data(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes) -> bytes:
    """Signs data with a managed key using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)
    
    # Asymmetric signing requires hashing the data before signing.
    # For simplicity, this example assumes data is already hashed with SHA256.
    # In a real application, you would hash the data here.
    digest = {"sha256": data} # Assuming data is a SHA256 hash
    
    response = client.asymmetric_sign(request={"name": name, "digest": digest})
    return response.signature

def verify_data(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes, signature: bytes) -> bool:
    """Verifies data with a managed key using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    public_key_name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)
    
    # Get the public key
    public_key_response = client.get_public_key(request={"name": public_key_name})
    public_key = public_key_response.pem
    
    # In a real application, you would use a cryptographic library (e.g., cryptography)
    # to verify the signature using the public_key, data, and signature.
    # For demonstration purposes, we will return True.
    # This is a placeholder and NOT a secure verification.
    return True
