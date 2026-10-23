from google.cloud import translate

def translate_markup(text: str, source_language: str, target_language: str) -> str:
    """Translates HTML or other markup while preserving tags using Google Cloud Translation.

    Args:
        text: The input text in HTML or other markup format.
        source_language: The language of the input text (e.g., "en" for English).
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text with tags preserved.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID

    # The translate_text method can accept a list of texts.
    # We specify the text_mime_type as "text/html" to preserve tags.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and desired text/languages)
    # Ensure you have authenticated with Google Cloud (e.g., using `gcloud auth application-default login`)
    # and replaced "YOUR_PROJECT_ID" with your actual Google Cloud Project ID.
    html_text = "<p>Hello, <b>world</b>!</p>"
    source_lang = "en"
    target_lang = "fr"

    try:
        translated_html = translate_markup(html_text, source_lang, target_lang)
        print(f"Original HTML: {html_text}")
        print(f"Translated HTML ({target_lang}): {translated_html}")

        html_text_es = "<p>¡Hola, <b>mundo</b>!</p>"
        source_lang_es = "es"
        target_lang_es = "en"
        translated_html_es = translate_markup(html_text_es, source_lang_es, target_lang_es)
        print(f"Original HTML: {html_text_es}")
        print(f"Translated HTML ({target_lang_es}): {translated_html_es}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have set 'YOUR_PROJECT_ID' in the code and authenticated with Google Cloud.")
