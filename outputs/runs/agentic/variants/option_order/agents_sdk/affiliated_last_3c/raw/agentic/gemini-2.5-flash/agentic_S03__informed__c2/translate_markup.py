import os
from google.cloud import translate_v2 as translate

def translate_markup(html_text: str, target_language: str, source_language: str = None) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(
        html_text,
        target_language=target_language,
        source_language=source_language,
        format='html',
        model='nmt' # Neural Machine Translation model
    )
    return result['translatedText']

if __name__ == '__main__':
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    html_content = "<p>Hello <b>World</b>!</p>"
    translated_html = translate_markup(html_content, "de")
    print(f"Translated HTML: {translated_html}")
