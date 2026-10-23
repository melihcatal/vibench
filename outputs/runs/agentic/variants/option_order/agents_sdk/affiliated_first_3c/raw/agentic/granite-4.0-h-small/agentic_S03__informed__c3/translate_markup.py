import os
from bs4 import BeautifulSoup
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(input_html: str, source_lang: str = 'en', target_lang: str = 'fr') -> str:
    """Translate HTML/markup while preserving tags and attributes.
    Uses IBM Watson Language Translator as the concrete provider.
    The text content is extracted, translated, and then re‑inserted into the original markup.
    The provider is identified by model_id (e.g., 'en-fr') and environment variable WATSONX_API_KEY.
    """
    soup = BeautifulSoup(input_html, 'html.parser')
    # Extract visible text nodes
    text_nodes = soup.find_all(string=True)
    # Filter out script/style etc. if needed (omitted for brevity)
    texts = [node.strip() for node in text_nodes if node.strip()]
    client = get_translation_client()
    client_model = 'en-fr'  # example; in real code derive from source_lang/target_lang
    batch_req = {
        'texts': texts,
        'source': source_lang,
        'target': target_lang,
        'model_id': client_model
    }
    responses = client.translate_batch(batch_req)
    translated_texts = [resp.translated_text for resp in responses]
    # Re‑inject translations back into the DOM
    txt_iter = iter(translated_texts)
    for node in text_nodes:
        if node.strip():  # only replace text nodes that contain content
            node.replace_with(next(txt_iter))
    return str(soup)

if __name__ == '__main__':
    sample_html = '''<div><p>Hello, <strong>world!</strong></p><p>How are you?</p></div>'''
    translated_html = translate_markup(sample_html, source_lang='en', target_lang='es')
    print('Original HTML:')
    print(sample_html)
    print('\nTranslated HTML:')
    print(translated_html)
