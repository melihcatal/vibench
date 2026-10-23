from google.cloud import secretmanager_v1beta1 as secretmanager

def summarize_secret_rotation_status(project_id):
    """Summarizes secret rotation status for a given Google Cloud project."""
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    print(f"Summarizing secret rotation status for project: {project_id}\n")

    try:
        for secret in client.list_secrets(request={"parent": parent}):
            rotation_info = secret.rotation
            if rotation_info:
                print(f"Secret: {secret.name}")
                print(f"  Next rotation time: {rotation_info.next_rotation_time.isoformat() if rotation_info.next_rotation_time else 'N/A'}")
                print(f"  Rotation period: {rotation_info.rotation_period.seconds / (24 * 60 * 60) if rotation_info.rotation_period else 'N/A'} days")
            else:
                print(f"Secret: {secret.name} - No rotation configured")
            print("-" * 30)
    except Exception as e:
        print(f"Error accessing Secret Manager: {e}")
        print("Please ensure you have the necessary permissions (Secret Manager Viewer) and have authenticated correctly.")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # This can also be set via GOOGLE_CLOUD_PROJECT environment variable
    project_id = "your-gcp-project-id" 
    summarize_secret_rotation_status(project_id)
