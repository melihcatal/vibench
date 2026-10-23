from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]


if __name__ == "__main__":
    # This is an example of how to use the function.
    # In a real application, you would load these from configuration or environment variables.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/google_credentials.json"
    )

    text_to_translate = "Hello, world!"
    target_lang = "es"
    translated = translate_text(text_to_translate, target_lang)
    print(f"Original: {text_to_translate}, Translated: {translated}")
