from google.cloud import translate_v3


def get_translation_client(config):
    client = translate_v3.TranslationServiceClient()
    return client