import os
from security_client import SecretManagementClient


def fetch_db_secret(secret_id: str) -> str:
    client = SecretManagementClient()
    payload = client.get_secret_payload(secret_id=secret_id)
    if payload and payload.data:
        return payload.data.decode("utf-8")
    raise ValueError(f"Database secret for {secret_id} not found or is empty.")


if __name__ == "__main__":
    # Example usage: Replace 'your-db-connection-secret-id' with your actual secret ID
    # And ensure GOOGLE_CLOUD_PROJECT environment variable is set
    try:
        db_secret = fetch_db_secret("your-db-connection-secret-id")
        # In a real application, you would use this secret to connect to a database
        print(f"Successfully fetched DB Secret (truncated): {db_secret[:10]}...")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
