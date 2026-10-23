from google.cloud import translate_v2 as translate

def translate_query(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation.
    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.
    Returns:
        The translated text.
    """
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and desired text/language)
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    query = "Hello, how are you?"
    target_lang = "es"  # Translate to Spanish

    if project_id == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_query = translate_query(query, target_lang, project_id)
        print(f"Original query: {query}")
        print(f"Translated query ({target_lang}): {translated_query}")
