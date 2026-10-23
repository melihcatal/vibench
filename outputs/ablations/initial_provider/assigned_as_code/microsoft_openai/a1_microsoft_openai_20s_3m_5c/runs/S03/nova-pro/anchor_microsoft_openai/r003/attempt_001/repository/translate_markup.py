import re


def translate_markup(markup, config=None):
    config = config or {}
    # Extract text from markup
    text = re.sub('<[^<]+?>', '', markup)
    # Translate text
    translated_text = translate_text({'text': text, 'source_language': 'en', 'target_language': 'es'}, config)
    # Replace original text with translated text in markup
    translated_markup = re.sub(re.escape(text), translated_text['text'], markup)
    return translated_markup