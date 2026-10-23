from google.cloud.translate_v2 import Translation


def normalize_response(response):
    return response["translatedText"]
