import re
from translation_client import translate_text

def translate_markup(markup, target_language):
    tags = re.findall(r'<[^>]+>', markup)
    content = re.sub(r'<[^>]+>', '', markup)
    translated_content = translate_text(content, target_language)
    translated_markup = translated_content
    for tag in tags:
        translated_markup = translated_markup.replace(content, tag + translated_content)
    return translated_markup