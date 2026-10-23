from google.cloud import translate_v2 as translate
import os


def batch_translate(
    texts: list[str], target_language: str, source_language: str = None
) -> list[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = translate.Client()
    translated_texts = []
    for text in texts:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
        translated_texts.append(result["translatedText"])
    return translated_texts


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/google_credentials.json"
    )

    texts_to_translate = ["Hello", "world", "How are you?"]
    target_lang = "fr"
    translated_list = batch_translate(texts_to_translate, target_lang)
    print(f"Original: {texts_to_translate}, Translated: {translated_list}")
