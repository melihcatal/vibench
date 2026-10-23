from google.cloud import translate_v3 as translate

def translate_html_with_google_cloud(
    text: str,
    project_id: str,
    source_language_code: str,
    target_language_code: str,
) -> str:
    """Translates HTML text using the Google Cloud Translation API, preserving tags.

    Args:
        text: The HTML text to translate.
        project_id: The ID of your Google Cloud project.
        source_language_code: The language code of the input text (e.g., "en-US").
        target_language_code: The language code to translate the text to (e.g., "es").

    Returns:
        The translated HTML text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        source_language_code=source_language_code,
        target_language_code=target_language_code,
        mime_type="text/html",  # Specify HTML format
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and desired text)
    your_project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your Google Cloud Project ID
    html_to_translate = "<p>Hello, <b>world</b>!</p>"
    source_lang = "en"
    target_lang = "es"

    if your_project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
        print("You also need to set up authentication for Google Cloud. See: https://cloud.google.com/docs/authentication/getting-started")
    else:
        try:
            translated_html = translate_html_with_google_cloud(
                html_to_translate, your_project_id, source_lang, target_lang
            )
            print(f"Original HTML: {html_to_translate}")
            print(f"Translated HTML: {translated_html}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure your Google Cloud Project ID is correct and authentication is set up.")
