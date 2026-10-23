from google.cloud import translate_v2 as translate


def normalize_response(response):
    return response["translatedText"]


def create_translation_request(text, target_language):
    return {"text": text, "target_language": target_language}
