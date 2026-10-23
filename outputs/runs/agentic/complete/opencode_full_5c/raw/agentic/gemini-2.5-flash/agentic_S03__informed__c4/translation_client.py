import os
from google.cloud import translate_v3beta1 as translate


def get_translation_client():
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or the default service account when running in a GCP environment.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    return translate.TranslationServiceClient()


def get_project_id():
    # Attempt to get project ID from environment variable or gcloud config
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        try:
            import google.auth

            _, project_id = google.auth.default()
        except Exception:
            pass  # Fallback to None if not found
    return project_id
