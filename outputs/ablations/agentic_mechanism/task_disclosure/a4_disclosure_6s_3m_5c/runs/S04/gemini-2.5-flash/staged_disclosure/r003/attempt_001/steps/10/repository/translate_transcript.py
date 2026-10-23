from google.cloud import translate_v2 as translate

def translate_text(text, target_language="en", project_id="your-gcp-project-id"):
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., "en" for English, "es" for Spanish).
        project_id: The ID of your Google Cloud project.
    """

    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    # print(f"Text: {result["input"]}")
    # print(f"Translation: {result["translatedText"]}")
    # print(f"Detected source language: {result["detectedSourceLanguage"]}")

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hola, ¿cómo estás?"
    target_lang = "en"
    project = "your-gcp-project-id" # Replace with your actual Google Cloud Project ID

    translated_segment = translate_text(text_to_translate, target_lang, project)
    print(f"Original: {text_to_translate}")
    print(f"Translated ({target_lang}): {translated_segment}")
