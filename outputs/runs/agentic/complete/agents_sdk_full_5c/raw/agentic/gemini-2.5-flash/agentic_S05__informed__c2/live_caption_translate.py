import os
from google.cloud import translate_v3 as translate

def translate_text_with_glossary(project_id: str, text: str, target_language: str, source_language: Optional[str] = None) -> str:
    """
    Translates a given text into the target language using Google Cloud Translation.
    This function allows for optional source language specification and glossary usage (though glossary is not implemented here).
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable or default ADC.

    Args:
        project_id: The Google Cloud Project ID.
        text: The text to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).
        source_language: The language code of the input text (e.g., "en" for English). Auto-detected if None.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Glossary is not directly used in this basic example but the function name suggests it.
    # For glossary usage, you would construct a GlossaryConfig object.

    request = translate.TranslateTextRequest(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
    )

    response = client.translate_text(request=request)

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text


def live_caption_translator(project_id: str, caption_chunk: str, target_language: str, source_language: Optional[str] = None) -> str:
    """
    Translates a single live caption chunk.
    """
    if not caption_chunk.strip():
        return ""
    try:
        translated_caption = translate_text_with_glossary(project_id, caption_chunk, target_language, source_language)
        return translated_caption
    except Exception as e:
        print(f"Error translating caption: {e}")
        return f"[Translation Error: {e}]"


if __name__ == "__main__":
    # Set your Google Cloud Project ID
    # GOOGLE_CLOUD_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    # if not GOOGLE_CLOUD_PROJECT_ID:
    #     print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
    #     exit()

    # example_caption = "Hello world, this is a live caption stream."
    # target_lang = "es"

    # translated = live_caption_translator(GOOGLE_CLOUD_PROJECT_ID, example_caption, target_lang, source_language="en")
    # print(f"Original: {example_caption}")
    # print(f"Translated ({target_lang}): {translated}")

    # example_caption_fr = "Bonjour le monde, ceci est un flux de sous-titres en direct."
    # target_lang_en = "en"
    # translated_en = live_caption_translator(GOOGLE_CLOUD_PROJECT_ID, example_caption_fr, target_lang_en, source_language="fr")
    # print(f"Original: {example_caption_fr}")
    # print(f"Translated ({target_lang_en}): {translated_en}")
    pass
