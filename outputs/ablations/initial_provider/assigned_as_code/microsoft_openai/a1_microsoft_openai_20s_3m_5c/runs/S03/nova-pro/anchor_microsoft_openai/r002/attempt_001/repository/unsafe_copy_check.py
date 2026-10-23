import re
import translation_client

def unsafe_copy_check(translation):
    client = translation_client.TranslationClient()
    unsafe_patterns = [r'\b(badword1|badword2|badword3)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, translation['text'], re.IGNORECASE):
            return {'unsafe': True, 'text': translation['text'], 'source_language': translation['source_language'], 'target_language': translation['target_language']}
    return {'unsafe': False, 'text': translation['text'], 'source_language': translation['source_language'], 'target_language': translation['target_language']}