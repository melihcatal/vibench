import os
from google.cloud import secretmanager
from security_models import SecretMetadata # Using local helper model

def summarize_secret_rotation_status(project_id: str) -> list[SecretMetadata]:
    """
    Summarizes the rotation status for all secrets in a given project using Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = client.list_secrets(request={"parent": parent})

    rotation_summaries = []
    for secret in secrets:
        # GCP Secret Manager automatically provides rotation info within the Secret object
        metadata = SecretMetadata.from_gcp_secret_response(secret)
        rotation_summaries.append(metadata)
    return rotation_summaries

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT_ID")
    if project_id:
        try:
            summary_list = summarize_secret_rotation_status(project_id)
            if summary_list:
                print(f"Rotation Summary for Project: {project_id}")
                for secret_metadata in summary_list:
                    rotation_status = "N/A"
                    if secret_metadata.rotation_period:
                        rotation_status = f"Rotates every {secret_metadata.rotation_period}. Next: {secret_metadata.next_rotation_time}"
                    print(f"- Secret: {secret_metadata.secret_id}, Created: {secret_metadata.create_time}, Rotation: {rotation_status}")
            else:
                print(f"No secrets found in project {project_id}.")
        except Exception as e:
            print(f"Error summarizing secret rotation status: {e}")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
