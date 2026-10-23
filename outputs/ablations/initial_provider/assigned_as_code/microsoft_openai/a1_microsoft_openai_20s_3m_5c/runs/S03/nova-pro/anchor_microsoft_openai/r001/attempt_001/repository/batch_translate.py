from.translation_client import translation_client, normalize_response

def batch_translate(texts, target_language):
    client = translation_client()
    responses = client.translate(texts, target_language=target_language, timeout=30)
    return [normalize_response(response) for response in responses]