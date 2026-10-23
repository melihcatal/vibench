from security_client import SecretManagerClient
from security_models import Secret, SecretVersion
import os

def summarize_secret_rotation_status() -> list[Secret]:
    """Summarizes secret rotation status for all secrets in the project using Google Secret Manager."""
    client = SecretManagerClient()
    secrets_summary = []
    for secret_data in client.list_secrets():
        secret_id = secret_data['name'].split('/')[-1]
        versions_data = client.list_secret_versions(secret_id)
        versions = [
            SecretVersion(
                name=v['name'],
                state=v['state'],
                create_time=v['create_time'],
                destroy_time=v['destroy_time']
            ) for v in versions_data
        ]
        secrets_summary.append(
            Secret(
                name=secret_data['name'],
                labels=secret_data['labels'],
                create_time=secret_data['create_time'],
                versions=versions
            )
        )
    return secrets_summary

if __name__ == "__main__":
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable before running
    # For example: export GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"
    if "GOOGLE_CLOUD_PROJECT_ID" not in os.environ:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        try:
            summary = summarize_secret_rotation_status()
            for secret in summary:
                print(f"\nSecret: {secret.name}")
                print(f"  Labels: {secret.labels}")
                print(f"  Created: {secret.create_time}")
                print(f"  Versions:")
                for version in secret.versions:
                    print(f"    - {version.name} (State: {version.state}, Created: {version.create_time})")
        except Exception as e:
            print(f"Error summarizing secret rotation status: {e}")
