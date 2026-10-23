import os
from google.cloud import translate_v2 as translate
import re

def check_unsafe_content(text):
    client = translate.Client()
    result = client.translate(text, target_language='en')
    translated_text = result['translatedText']
    unsafe_patterns = [r'hate', r'violence']
    for pattern in unsafe_patterns:
        if re.search(pattern, translated_text, re.IGNORECASE):
            return True
    return False