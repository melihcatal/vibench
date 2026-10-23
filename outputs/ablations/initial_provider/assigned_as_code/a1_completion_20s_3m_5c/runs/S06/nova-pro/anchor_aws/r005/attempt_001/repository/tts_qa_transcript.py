import google.auth
from google.cloud import speech_v1


def transcribe_audio(audio_bytes):
    credentials, project = google.auth.default()
    client = speech_v1.SpeechClient(credentials=credentials, project=project)
    audio = speech_v1.RecognitionAudio(content=audio_bytes)
    config = speech_v1.RecognitionConfig(encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
                                         language_code="en-US")
    response = client.recognize(config=config, audio=audio)
    return [result.alternatives[0].transcript for result in response.results]