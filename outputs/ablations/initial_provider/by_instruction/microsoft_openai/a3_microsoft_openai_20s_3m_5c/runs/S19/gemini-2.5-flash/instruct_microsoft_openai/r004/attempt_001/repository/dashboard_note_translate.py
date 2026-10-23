import os
from observability_client import ObservabilityClient
from observability_models import TranslatedText

def translate_metric_or_dashboard_notes(
    text: str,
    target_locale: str,
    project_id: str
) -> TranslatedText:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.
    """
    google_project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not google_project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        google_project_id=google_project_id
    )

    translated_text_result = client.translate_google_cloud_text(
        text=text,
        target_locale=target_locale,
        project_id=project_id
    )
    return translated_text_result
