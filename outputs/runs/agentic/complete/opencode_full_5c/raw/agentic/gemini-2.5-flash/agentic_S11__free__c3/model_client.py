import os


def get_vertex_ai_project_location():
    # In a real application, these would come from environment variables or a config file.
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    return project, location
