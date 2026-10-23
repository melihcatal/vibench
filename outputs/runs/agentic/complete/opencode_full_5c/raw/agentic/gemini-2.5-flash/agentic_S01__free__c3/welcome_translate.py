import os
from google.cloud import translate_v3beta1
from identity_models import TranslationRequest, TranslationResponse
from identity_client import get_google_cloud_project_id


def welcome_translate(request: TranslationRequest) -> TranslationResponse:
    client = translate_v3beta1.TranslationServiceClient()
    project_id = request.project_id
    location = request.location  # "global" or specific region

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language_code,
            # Source language code can be auto-detected or specified
            # source_language_code="en",
        )
        translated_text = response.translations[0].translated_text
        return TranslationResponse(translated_text=translated_text)
    except Exception as e:
        raise RuntimeError(f"Google Cloud Translation failed: {e}")


if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT_ID env var and auth setup)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    os.environ["GOOGLE_CLOUD_PROJECT_ID"] = "YOUR_GCP_PROJECT_ID"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    try:
        translate_request = TranslationRequest(
            text="Welcome to our service!",
            target_language_code="es",
            project_id=get_google_cloud_project_id(),
        )
        response = welcome_translate(translate_request)
        print(f"Original: '{translate_request.text}'")
        print(
            f"Translated ({translate_request.target_language_code}): '{response.translated_text}'"
        )
    except Exception as e:
        print(f"Error during translation: {e}")
