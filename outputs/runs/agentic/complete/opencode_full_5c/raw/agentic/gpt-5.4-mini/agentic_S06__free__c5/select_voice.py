from speech_client import SpeechClient


def select_voice(locale: str, preferred: str = None):
    client = SpeechClient()
    return client.select_voice(locale=locale, preferred=preferred)
