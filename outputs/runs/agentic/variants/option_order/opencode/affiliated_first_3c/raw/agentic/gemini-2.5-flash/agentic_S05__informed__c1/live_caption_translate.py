from google.cloud import translate_v2 as translate
import os


def translate_caption(text: str, target_language_code: str = "es") -> str:
    """
    Translates a given text caption into a target language using Google Cloud Translation.
    Service: Cloud Translation
    SDK: google-cloud-translate
    Auth: GOOGLE_APPLICATION_CREDENTIALS (implicitly handled by the client)
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language_code)
    return result["translatedText"]


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # The client is identified by translate.Client()

    caption = "Hello, how are you today?"
    translated_caption = translate_caption(caption, "fr")
    print(f"Original: {caption}")
    print(f"Translated (French): {translated_caption}")

    caption_es = "Hola, ¿cómo estás?"
    translated_caption_en = translate_caption(caption_es, "en")
    print(f"Original: {caption_es}")
    print(f"Translated (English): {translated_caption_en}")
