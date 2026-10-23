import re
import translation_client

def translate_markup(markup, source_language, target_language, config=None):
    tag_pattern = re.compile(r'<[^>]+>')
    tags = tag_pattern.findall(markup)
    translated_markup = ''
    for tag in tags:
        translated_markup += tag
    inner_text = re.sub(tag_pattern, '', markup)
    translated_inner_text = translation_client.translate_text({'text': inner_text, 'source_language': source_language, 'target_language': target_language}, config)['text']
    translated_markup += translated_inner_text
    return translated_markup