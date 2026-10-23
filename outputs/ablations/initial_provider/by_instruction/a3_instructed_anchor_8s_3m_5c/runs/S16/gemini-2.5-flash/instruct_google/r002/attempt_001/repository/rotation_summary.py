import os
from security_client import SecurityClient
from security_models import SecretMetadata

def get_secret_rotation_summary(project_id: str, secret_id: str) -> SecretMetadata:
    client = SecurityClient()
    secret_metadata = client.get_secret_metadata(project_id, secret_id)
    return secret_metadata

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_to_summarize_id = "my-api-key"
    # summary = get_secret_rotation_summary(project_id, secret_to_summarize_id)
    # print(f"Secret Rotation Summary for {secret_to_summarize_id}:\n  Create Time: {summary.create_time}\n  Next Rotation: {summary.rotation_time}\n  Labels: {summary.labels}")
