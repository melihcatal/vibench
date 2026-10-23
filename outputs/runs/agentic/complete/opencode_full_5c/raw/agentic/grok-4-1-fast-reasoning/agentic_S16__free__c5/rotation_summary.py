import os
from google.cloud import secretmanager


def summarize_rotation_status(
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT"),
) -> str:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    summary_lines = []
    for secret in client.list_secrets(request={"parent": parent}).secrets:
        secret_name = secret.name
        try:
            secret_detail = client.get_secret(request={"name": secret_name})
            rotation = secret_detail.rotation
            if rotation:
                next_time = (
                    rotation.next_rotation_time.ToDatetime()
                    if hasattr(rotation, "next_rotation_time")
                    and rotation.next_rotation_time
                    else "unknown"
                )
                summary_lines.append(
                    f"{secret_name}: Rotation enabled, next rotation: {next_time}"
                )
            else:
                summary_lines.append(f"{secret_name}: Rotation disabled")
        except Exception as e:
            summary_lines.append(f"{secret_name}: Error checking rotation - {str(e)}")
    return "\n".join(summary_lines)
