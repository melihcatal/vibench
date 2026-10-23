from google.cloud import texttospeech_v1 as texttospeech


def platform_brief_audio(text: str) -> dict:
    client = texttospeech.TextToSpeechClient()
    return {"provider": "google", "audio_config": "MP3", "client": client.__class__.__name__, "text": text}
