import os
import re
from google.cloud import translate_v2 as translate

def translate_markup(html, target_language='es'):
    # Simple tag-preserving translation: extract tag parts, translate only text nodes
    def replace_text(match):
        txt = match.group(2)
        translated = translate.Client().translate(txt, target_language=target_language)['translatedText']
        return f"{match.group(1)}{translated}{match.group(3)}"
    # Pattern: <tag>text</tag> or <tag/> style
    pattern = re.compile(r'(</?[^>]+>)|(<!--.*?-->|<!--|-->|[^<]+)')
    translated_html = pattern.sub(replace_text, html)
    return translated_html

if __name__ == '__main__':
    sample_html = "<p>Hello, <b>world</b>!</p>"
    print(translate_markup(sample_html, 'fr'))