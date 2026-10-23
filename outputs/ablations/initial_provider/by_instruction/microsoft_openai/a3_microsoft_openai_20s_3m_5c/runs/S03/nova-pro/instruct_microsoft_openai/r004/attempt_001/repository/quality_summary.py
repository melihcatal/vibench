from translation_client import TranslationClient

def quality_summary(text, to_language):
    client = TranslationClient()
    translated_text = client.translate(text, to_language)
    # Placeholder for quality summary logic
    return f'Quality summary for translation of {text} to {to_language}.'