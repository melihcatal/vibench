import re
import translation_client

def translate_markup(markup, source_language, target_language, config=None):
    client = translation_client.TranslationClient(config)
    tags = re.findall(r'<[^>]+>', markup)
    content = re.sub(r'<[^>]+>', '', markup)
    translation = client.translate_text({'text': content, 'source_language': source_language, 'target_language': target_language})
    translated_markup = translation['text']
    for tag in tags:
        translated_markup = re.sub(r'(<[^>]+>)', tag, translated_markup, 1)
    return {'markup': translated_markup, 'source_language': source_language, 'target_language': target_language}