from google.cloud import translate_v2 as translate


def batch_translate(texts, target_language):
    client = translate.Client()
    results = client.translate(texts, target_language=target_language)
    return [result["translatedText"] for result in results["translations"]]
