from google.cloud import translate_v2 as translate
import os


def translate_dictionary_values(
    data: dict, target_language: str, source_language: str = None
) -> dict:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = translate.Client()
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            result = client.translate(
                value, target_language=target_language, source_language=source_language
            )
            translated_data[key] = result["translatedText"]
        else:
            translated_data[key] = value  # Preserve non-string values
    return translated_data


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/google_credentials.json"
    )

    dict_to_translate = {"greeting": "Hello", "farewell": "Goodbye", "number": 123}
    target_lang = "it"
    translated_dict = translate_dictionary_values(dict_to_translate, target_lang)
    print(f"Original: {dict_to_translate}, Translated: {translated_dict}")
