
from google.cloud import translate

def translate_text(text, project_id="your-gcp-project-id", target_language="en"):
    """Translates text into the target language."""

    client = translate.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    return translated_texts

if __name__ == "__main__":
    # Replace with your actual project ID and desired text/language
    project_id = "your-gcp-project-id"
    text_to_translate = "Hola, ¿cómo estás?"
    target_language = "es" # For example, translate to Spanish

    # Example usage:
    translated_result = translate_text(text_to_translate, project_id, target_language)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text: {translated_result}")

