import os
from google.cloud import translate_v3
from google.api_core.client_options import ClientOptions

def get_translation_service_client():
    # The client is configured to use the regional endpoint for better performance or data residency
    # For a global endpoint, you would remove the client_options or set api_endpoint to 'translate.googleapis.com'
    client_options = ClientOptions(api_endpoint="translate.googleapis.com")
    client = translate_v3.TranslationServiceClient(client_options=client_options)
    return client

def get_project_id():
    # It's recommended to set the GOOGLE_CLOUD_PROJECT environment variable
    # or ensure gcloud is configured with a default project.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback to default project if GOOGLE_CLOUD_PROJECT is not set
        # In a real-world scenario, you might want to raise an error or configure explicitly
        print("WARNING: GOOGLE_CLOUD_PROJECT environment variable not set. Using default project from gcloud config.")
        try:
            import google.auth
            _, project_id = google.auth.default()
        except Exception as e:
            raise RuntimeError("Could not determine Google Cloud project ID. Please set GOOGLE_CLOUD_PROJECT environment variable or configure gcloud CLI.") from e
    return project_id

def get_location():
    # Default to 'global' if not specified, but 'us-central1' or other regions can be used
    return os.getenv("GOOGLE_CLOUD_LOCATION", "global")
