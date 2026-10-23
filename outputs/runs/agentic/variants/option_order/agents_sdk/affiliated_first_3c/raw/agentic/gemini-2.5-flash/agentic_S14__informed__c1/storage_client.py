from google.cloud import storage
import os

def get_storage_client():
    """Provides a Google Cloud Storage client instance."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    return storage.Client()

if __name__ == '__main__':
    # Example usage
    # client = get_storage_client()
    # print(f"Google Cloud Storage client created: {client}")
    pass
