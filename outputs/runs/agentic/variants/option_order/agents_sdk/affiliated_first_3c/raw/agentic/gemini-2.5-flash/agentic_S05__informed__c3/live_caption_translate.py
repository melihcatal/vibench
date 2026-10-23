from google.cloud import translate

def translate_caption(text: str, target_language_code: str = "es") -> str:
    """Translates a given text caption into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    project_id = client.project_path(client.project_name)
    # The client.project_name is typically loaded from GOOGLE_APPLICATION_CREDENTIALS or environment variables.
    # For local testing without a specific project set, you might need to specify it or handle the default.

    response = client.translate_text(
        request={
            "parent": f"projects/{project_id}", # The project_id needs to be resolved correctly.
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # The actual project ID might be extracted from environment or configured.
    # For this example, a placeholder project_id is used. In a real application,
    # ensure `client.project_name` correctly identifies your Google Cloud project.
    # A more robust way to get the project ID is using google.auth.default() or explicit project parameter.
    # For this file, let's assume GOOGLE_APPLICATION_CREDENTIALS are set and provide a project_id.
    # If running locally, you might need to set GOOGLE_CLOUD_PROJECT environment variable.

    # Fallback/placeholder for project_id if it cannot be dynamically determined by the client
    # In a real application, you would ensure project_id is correctly set.
    try:
        # Attempt to get project ID from the client configuration
        project_id = client.project_path(client.project_name).split('/')[-1]
    except Exception:
        # Fallback for demonstration if client.project_name is not configured with a specific project
        # In a real application, replace 'your-gcp-project-id' with your actual project ID
        project_id = "your-gcp-project-id" # Placeholder

    response = client.translate_text(
        request={
            "parent": f"projects/{project_id}/locations/global",
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
