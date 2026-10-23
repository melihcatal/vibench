from bs4 import BeautifulSoup
from.translation_client import translation_client, normalize_response

def translate_markup(markup, target_language):
    soup = BeautifulSoup(markup, 'html.parser')
    for tag in soup.find_all(text=True):
        if tag.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
            translated_text = translation_client().translate(tag, target_language=target_language, timeout=30)
            tag.replace_with(translated_text['translatedText'])
    return str(soup)