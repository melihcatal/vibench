from speech_client import SpeechClient


def save_audio(audio: bytes, destination):
    client = SpeechClient()
    return client.save_audio(audio, destination)
