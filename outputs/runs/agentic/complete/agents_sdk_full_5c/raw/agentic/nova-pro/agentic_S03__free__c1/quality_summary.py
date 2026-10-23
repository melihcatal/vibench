from google.cloud import translate_v2 as translate

def summarize_quality(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {'quality': 'high' if result['detectedSourceLanguage'] == target_language else 'low'}