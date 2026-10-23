from google.cloud import translate_v3beta1 as translate
import os


def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates the input text into the target language using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    text_to_translate = "Hello, how are you?"
    target_lang = "es"
    # translated = translate_text(text_to_translate, target_lang, project_id)
    # print(f"Original: {text_to_translate}")
    # print(f"Translated ({target_lang}): {translated}")
