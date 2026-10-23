from translator import translate

def record_translate(document, target_language):
    text = document.get('text', '')
    return translate(text, target_language)