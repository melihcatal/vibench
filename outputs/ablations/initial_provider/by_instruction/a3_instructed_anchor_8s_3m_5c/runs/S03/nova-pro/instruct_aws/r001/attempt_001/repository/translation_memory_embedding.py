from translation_client import get_translate_client

def embed_translation_memory(text):
    client = get_translate_client()
    response = client.embed_text(
        Text=text,
        LanguageCode='en'
    )
    return response['Embedding']