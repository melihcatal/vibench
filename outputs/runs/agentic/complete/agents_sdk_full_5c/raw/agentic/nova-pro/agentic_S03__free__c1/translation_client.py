from google.cloud import translate_v2 as translate

def get_client():
    return translate.Client()