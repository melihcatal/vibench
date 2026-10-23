import os
from google.cloud import translate
from messaging_models import TranslatedPayload


def translate_message_text(
    message_id: str, text: str, target_language: str = "es"
) -> TranslatedPayload:
    """
    Translates customer-facing message payload text using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslatedPayload(
        message_id=message_id,
        original_text=text,
        translated_text=translated_text,
        target_language=target_language,
    )


if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up (e.g., path to a service account key file)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    original_text = "Hello, how are you today?"
    translated_result = translate_message_text("msg-translate-1", original_text, "fr")
    print(f"Translation Result: {translated_result}")

    original_text_es = "Me gustaría pedir una pizza."
    translated_result_en = translate_message_text(
        "msg-translate-2", original_text_es, "en"
    )
    print(f"Translation Result (Spanish to English): {translated_result_en}")
