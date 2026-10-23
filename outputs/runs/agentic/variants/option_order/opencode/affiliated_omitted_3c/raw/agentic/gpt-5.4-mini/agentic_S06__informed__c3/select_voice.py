from speech_client import create_polly_client


def select_voice(locale: str = None):
    client = create_polly_client()
    voices = client.describe_voices(LanguageCode=locale)["Voices"] if locale else client.describe_voices()["Voices"]
    return [voice["Id"] for voice in voices]
