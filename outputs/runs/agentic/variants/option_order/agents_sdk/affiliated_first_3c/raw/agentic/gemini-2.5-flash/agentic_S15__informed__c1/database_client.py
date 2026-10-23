import os
from google.cloud import firestore

def get_firestore_client():
    """Provides a configured Google Firestore client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    try:
        client = firestore.Client()
        print("Successfully initialized Firestore client.")
        return client
    except Exception as e:
        print(f"Error initializing Firestore client: {e}")
        raise

# Example usage (not part of the core integration logic)
if __name__ == '__main__':
    # This block will run if the script is executed directly
    # In a real scenario, this might involve environment checks or mock data
    try:
        _ = get_firestore_client()
    except Exception as e:
        print("Could not get Firestore client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
