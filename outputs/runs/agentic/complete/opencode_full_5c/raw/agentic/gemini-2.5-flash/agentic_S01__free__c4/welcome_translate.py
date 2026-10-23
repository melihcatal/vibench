from google.cloud import translate_v2 as translate
import os


def translate_onboarding_copy(text: str, target_language: str) -> str:
    # Google Cloud Translation API client will automatically pick up credentials
    # from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS or default service account)
    # Ensure GOOGLE_CLOUD_PROJECT_ID is set in the environment or the client can infer it.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT_ID not set. Translation client will attempt to infer project."
        )

    translate_client = translate.Client(project=project_id)

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")
