from google.cloud import translate_v2 as translate

def translate_client():
    return translate.Client()