import translation_client

def batch_translate(texts, source_language, target_language, config=None):
    translations = []
    for text in texts:
        payload = {'text': text, 'source_language': source_language, 'target_language': target_language}
        translation = translation_client.translate_text(payload, config)
        translations.append(translation['text'])
    return translations