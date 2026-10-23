from translation_client import get_translate_client

def check_unsafe_copy(text):
    client = get_translate_client()
    response = client.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response['Labels']