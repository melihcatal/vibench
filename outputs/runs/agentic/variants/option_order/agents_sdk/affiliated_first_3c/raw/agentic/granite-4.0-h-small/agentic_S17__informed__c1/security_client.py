import os
from google.cloud import kms

def get_kms_client():
    """Creates and returns a Google Cloud KMS client using environment credentials."""
    # GOOGLE_APPLICATION_CREDENTIALS env var expected to point to service account JSON
    return kms.KeyManagementServiceClient()


def generate_data_encryption_key(byte_length):
    """Generates a random data encryption key (local) of specified byte length."""
    # Use OS urandom for simplicity; for production consider a CSPRNG library
    import secrets
    return secrets.token_bytes(byte_length)
