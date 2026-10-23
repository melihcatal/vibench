from google.cloud import translate_v3 as translate
from bs4 import BeautifulSoup

def translate_html_markup(html_content: str, source_language: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/your-project-id"  # Replace with your Google Cloud Project ID

    soup = BeautifulSoup(html_content, 'html.parser')

    for text_node in soup.find_all(string=True):
        if text_node.strip():  # Only translate non-empty text
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text_node.strip()],
                    "mime_type": "text/html",
                    "source_language_code": source_language,
                    "target_language_code": target_language,
                }
            )
            translated_text = response.translations[0].translated_text
            text_node.replace_with(translated_text)

    return str(soup)