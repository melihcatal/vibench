import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_log_message(log_message, to_language):
    credential = TranslatorCredential(os.getenv('TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint=os.getenv('TRANSLATOR_ENDPOINT'), credential=credential)
    result = client.translate([log_message], to_language)[0]
    return result.translations[0].text

# Example usage:
# translate_log_message('Error occurred during user login', 'es')