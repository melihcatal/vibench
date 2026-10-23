import os


def get_gcp_project() -> str:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    return project
