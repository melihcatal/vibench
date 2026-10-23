from translation_client import translate_text

def batch_translate(texts, target_language):
    translations = []
    for text in texts:
        translation = translate_text(text, target_language)
        translations.append(translation)
    return translations