from translation_client import client

def check_unsafe_content(text: str) -> bool:
    response = client.translations.check_unsafe_content(text)
    return response['is_unsafe']