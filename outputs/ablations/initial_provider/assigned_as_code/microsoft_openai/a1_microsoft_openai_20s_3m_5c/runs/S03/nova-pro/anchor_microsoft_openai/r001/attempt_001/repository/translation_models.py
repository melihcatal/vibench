from google.cloud import translate_v2 as translate

def translation_client():
    client = translate.Client()
    return client