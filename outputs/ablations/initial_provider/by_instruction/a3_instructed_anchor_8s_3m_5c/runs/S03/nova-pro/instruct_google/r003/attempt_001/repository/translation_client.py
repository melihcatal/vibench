from google.cloud import translate_v2 as translate

def get_translate_client():
    return translate.Client()