from translation_client import get_translate_client
from translation_models import normalize_response
from bs4 import BeautifulSoup

def translate_markup(markup, target_language):
    soup = BeautifulSoup(markup, 'html.parser')
    texts = [tag.string for tag in soup.find_all(text=True) if tag.string]
    client = get_translate_client()
    translated_texts = client.translate_batch(texts, target_language=target_language)
    for i, tag in enumerate(soup.find_all(text=True)):
        if tag.string:
            tag.replace_with(normalize_response(translated_texts[i]).translated_text)
    return str(soup)
