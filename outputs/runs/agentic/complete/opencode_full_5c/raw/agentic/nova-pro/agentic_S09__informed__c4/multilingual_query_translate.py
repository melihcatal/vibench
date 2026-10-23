from google.cloud import translate_v2 as translate


def multilingual_query_translate(query, target_language):
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return result["translatedText"]
