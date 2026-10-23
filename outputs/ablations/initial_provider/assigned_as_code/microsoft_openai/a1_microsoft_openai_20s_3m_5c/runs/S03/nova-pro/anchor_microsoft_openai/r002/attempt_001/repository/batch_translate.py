import translation_client

def batch_translate(texts, source_language, target_language, config=None):
    client = translation_client.TranslationClient(config)
    payloads = [{'text': text, 'source_language': source_language, 'target_language': target_language} for text in texts]
    translations = [client.translate_text(payload) for payload in payloads]
    return [{'text': translation['text'], 'source_language': translation['source_language'], 'target_language': translation['target_language']} for translation in translations]