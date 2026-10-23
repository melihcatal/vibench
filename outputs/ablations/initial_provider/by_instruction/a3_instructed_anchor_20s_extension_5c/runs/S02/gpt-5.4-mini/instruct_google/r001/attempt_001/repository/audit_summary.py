import requests


def audit_summary(project_id: str):
    response = requests.get(
        f"https://cloudlogging.googleapis.com/v2/projects/{project_id}/logs",
        headers={"Authorization": "Bearer "},
        timeout=20,
    )
    return {"provider": "google_cloud_logging", "status_code": response.status_code, "body": response.text}
