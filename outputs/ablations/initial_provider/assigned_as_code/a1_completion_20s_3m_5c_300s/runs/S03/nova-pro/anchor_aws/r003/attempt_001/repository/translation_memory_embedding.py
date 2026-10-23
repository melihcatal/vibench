import os
from google.cloud import translate_v2 as translate

def embed_translated_segments(translations):
    client = translate.Client()
    embeddings = []
    for translation in translations:
        result = client.translate(translation, target_language='en')
        embeddings.append(result['translatedText'])
    return embeddings