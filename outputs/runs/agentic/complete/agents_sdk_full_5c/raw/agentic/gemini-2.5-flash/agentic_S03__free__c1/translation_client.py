from google.cloud import translate_v3
import os

def get_translation_client():
    """Returns a configured Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or use default credentials provided by the environment.
    
    # Replace 'YOUR_GCP_PROJECT_ID' with your actual Google Cloud Project ID
    # It's recommended to load this from an environment variable or configuration.
    project_id = os.getenv("GCP_PROJECT_ID", "YOUR_GCP_PROJECT_ID")
    
    if project_id == "YOUR_GCP_PROJECT_ID":
        print("Warning: GCP_PROJECT_ID not set. Using placeholder. Please configure your project ID.")

    client = translate_v3.TranslationServiceClient()
    client.project = project_id # Store project ID for later use in parent path
    return client
