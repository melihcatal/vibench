from google.cloud import kms
import os

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global" # Or specific region
    key_ring_id = "my-key-ring"
    key_id = "my-encryption-key"

    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # Example usage:
    # # Assuming you have ciphertext from encrypt_payload
    # # ciphertext_data = bytes.fromhex("...") 
    # try:
    #     plaintext = decrypt_payload(project_id, location_id, key_ring_id, key_id, ciphertext_data)
    #     print(f"Plaintext: {plaintext.decode('utf-8')}")
    # except Exception as e:
    #     print(f"Error decrypting: {e}")
