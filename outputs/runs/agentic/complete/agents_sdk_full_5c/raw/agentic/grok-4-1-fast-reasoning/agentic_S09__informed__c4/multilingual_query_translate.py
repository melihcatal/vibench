from google.cloud import translate_v2 as translate

def multilingual_query_translate(query: str, target_lang: str = "en") -> str:
    client = translate.Client()
    result = client.translate(query, target_language=target_lang)
    return result["translatedText"]