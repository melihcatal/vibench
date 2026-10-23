from google.cloud import translate_v3beta1 as translate

def get_translation_client():
    return translate.TranslationServiceClient()
