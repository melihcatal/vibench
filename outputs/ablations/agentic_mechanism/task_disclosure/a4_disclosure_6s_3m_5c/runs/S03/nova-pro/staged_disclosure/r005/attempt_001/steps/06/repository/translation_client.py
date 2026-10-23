import deepl

# Configuration
DEEPL_API_KEY = 'your-deepl-api-key'

# Client Helper Utilities
def translate_text(text, target_lang='EN'):
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text