import os
from google.cloud import translate_v3 as translate

def batch_translate_text(
    texts: list[str],
    target_language_code: str,
    project_id: str
) -> list[str]:
    """Translates a list of texts into the target language while preserving order.

    Args:
        texts: A list of strings to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.

    Returns:
        A list of translated strings, in the same order as the input texts.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
        mime_type="text/plain",  # Set to "text/html" for HTML input.
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)

    return translated_texts

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID and authenticate (e.g., via `gcloud auth application-default login`)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        texts_to_translate = ["Hello, world!", "How are you?", "This is a test."]
        target_lang = "es"  # Spanish

        print(f"Translating texts to {target_lang}: {texts_to_translate}")
        translated_result = batch_translate_text(texts_to_translate, target_lang, project_id)
        print(f"Translated texts: {translated_result}")
