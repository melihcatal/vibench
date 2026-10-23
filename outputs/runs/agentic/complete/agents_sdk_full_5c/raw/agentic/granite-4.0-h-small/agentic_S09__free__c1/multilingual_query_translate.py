# Translate queries to the target language before multilingual embedding search
from googletrans import Translator

translator = Translator()

def translate_query(query: str, target_lang: str = 'es') -> str:
    """Translate a query string to another language using Google Translate API."""
    try:
        translated = translator.translate(query, dest=target_lang)
        return translated.text
    except Exception as e:
        # Fallback to original if translation fails
        print('Translation failed:', e)
        return query

# Example usage:
# query_en = 'What is the capital of France?'
# query_es = translate_query(query_en, target_lang='es')
# print(query_es)
