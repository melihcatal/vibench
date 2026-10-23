from translation_client import client

def generate_audio_preview(text: str, language: str) -> str:
    response = client.translations.generate_audio_preview(text, language)
    return response['audio_url']