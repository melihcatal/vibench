from translation_client import TranslationClient

def unsafe_copy_check(text, to_language):
    client = TranslationClient()
    translated_text = client.translate(text, to_language)
    # Placeholder for unsafe copy check logic
    return f'Unsafe copy check for translation of {text} to {to_language}.'