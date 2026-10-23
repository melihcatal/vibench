from google.cloud import logging
import os

def get_logging_client():
    """
    Provides a configured Google Cloud Logging client.
    Requires GOOGLE_CLOUD_PROJECT environment variable to be set.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    return logging.Client(project=project_id)


from google.cloud import aiplatform

def get_aiplatform_text_client(project_id: str = None, location: str = "us-central1"):
    """
    Provides a configured Google Cloud AI Platform client for text models.
    Initializes the AI Platform SDK with a project and location.
    """
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set or project_id not provided.")

    # The aiplatform.init() call configures the default project and location for subsequent API calls.
    aiplatform.init(project=project_id, location=location)

    # No specific client object to return for text models, as we'll use aiplatform.TextGenerationModel.from_pretrained
    # or similar directly after init.
    print(f"Initialized Google Cloud AI Platform for project {project_id} in {location}.")
    return True # Indicate successful initialization
