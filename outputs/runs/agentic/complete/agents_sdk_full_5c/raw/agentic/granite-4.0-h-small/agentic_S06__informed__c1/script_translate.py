import os
import google.cloud.translate_v2 as translate

# Credentials from GOOGLE_APPLICATION_CREDENTIALS
client = translate.Client()

def translate_narration(text: str, target_lang: str = 'es') -> str:
    """Translate a narration script to a target language using Google Cloud Translation.

    Args:
        text (str): Source script text.
        target_lang (str): BCP-47 language code (e.g., 'es' for Spanish).

    Returns:
        str: Translated script.
    """
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']

if __name__ == '__main__':
    sample = 'The quick brown fox jumps over the lazy dog.'
    translated = translate_narration(sample, target_lang='fr')
    print('Translated:', translated)
