from translation_client import TranslationClient

def generate_localized_audio_preview(text, language):
    client = TranslationClient()
    audio_preview = client.generate_audio_preview(text, language)
    return audio_preview