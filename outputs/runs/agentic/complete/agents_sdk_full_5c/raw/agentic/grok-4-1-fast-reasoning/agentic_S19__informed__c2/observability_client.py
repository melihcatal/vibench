import os

def get_google_cloud_project() -> str:
    project = os.getenv('GOOGLE_CLOUD_PROJECT')
    if not project:
        raise ValueError('GOOGLE_CLOUD_PROJECT environment variable is required for Google Cloud Monitoring.')
    return project
