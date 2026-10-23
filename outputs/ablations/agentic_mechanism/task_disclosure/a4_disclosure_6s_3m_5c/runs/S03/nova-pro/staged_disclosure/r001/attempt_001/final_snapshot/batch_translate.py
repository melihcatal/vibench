from google.cloud import translate_v2 as translate

def batch_translate(texts):
    client = translate.Client()
    translations = []
    for text in texts:
        result = client.translate(text, target_language='es')
        translations.append(result['translatedText'])
    return translations