from google.cloud import translate_v3 as translate
import os

def translate_narration_script(
    project_id: str,
    text_content: str,
    target_language_code: str,
    source_language_code: Optional[str] = None
) -> str:
    """Translates narration scripts before synthesis using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap the text in a list for the API call
    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        model="projects/{project_id}/locations/{location}/models/general/nmt" # Example model
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and project ID)
    # PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    # if PROJECT_ID != "your-gcp-project-id":
    #     script_to_translate = "Hello, this is a narration script in English."
    #     translated = translate_narration_script(
    #         project_id=PROJECT_ID,
    #         text_content=script_to_translate,
    #         target_language_code="es",
    #         source_language_code="en"
    #     )
    #     print(f"Original: {script_to_translate}")
    #     print(f"Translated (es): {translated}")
    pass
