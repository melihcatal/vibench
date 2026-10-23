from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language."""
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and text)
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    text_to_translate = "This is an invoice note."
    target_lang = "es"  # Translate to Spanish

    if project_id == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_text = translate_text(text_to_translate, target_lang, project_id)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_text}")
