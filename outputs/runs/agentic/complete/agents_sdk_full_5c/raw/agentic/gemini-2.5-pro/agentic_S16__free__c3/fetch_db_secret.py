import os
from google.cloud import secretmanager
from security_client import get_gcp_credentials

def fetch_gcp_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str | None:
    """
    Fetches a database secret from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret to fetch (default is "latest").

    Returns:
        The secret payload as a string, or None if an error occurs.
    """
    try:
        credentials = get_gcp_credentials()
        client = secretmanager.SecretManagerServiceClient(credentials=credentials)

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        print(f"Error fetching secret from GCP Secret Manager: {e}")
        return None

# Example usage would be in a different file.
# if __name__ == "__main__":
#     gcp_project_id = os.environ.get("GCP_PROJECT_ID")
#     db_secret_name = os.environ.get("DB_SECRET_ID")

#     if gcp_project_id and db_secret_name:
#         db_connection_string = fetch_gcp_db_secret(gcp_project_id, db_secret_name)
#         if db_connection_string:
#             print("Successfully fetched database secret.")
#             # print(f"DB Connection String: {db_connection_string}") # Avoid printing secrets
#         else:
#             print("Failed to fetch database secret.")
#     else:
#         print("Please set GCP_PROJECT_ID and DB_SECRET_ID environment variables.")
