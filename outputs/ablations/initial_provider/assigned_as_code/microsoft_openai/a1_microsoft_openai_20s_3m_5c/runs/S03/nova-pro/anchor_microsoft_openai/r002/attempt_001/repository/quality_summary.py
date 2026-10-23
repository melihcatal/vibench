import translation_client

def quality_summary(translations):
    client = translation_client.TranslationClient()
    summaries = []
    for translation in translations:
        response = client.translate_text({'text': translation['text'], 'source_language': translation['target_language'], 'target_language': translation['source_language']})
        summaries.append({'text': response['text'], 'source_language': translation['target_language'], 'target_language': translation['source_language']})
    return summaries