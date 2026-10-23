import os
from deepl import Translator

os.environ['DEEPL_AUTH_KEY'] = 'your-deepl-auth-key'

deepl_translator = Translator()

def check_unsafe_copy(text, target_language='ES'):
    translation = deepl_translator.translate_text(text, target_lang=target_language)
    # Placeholder for actual unsafe content check logic
    return 'Unsafe content check result.'