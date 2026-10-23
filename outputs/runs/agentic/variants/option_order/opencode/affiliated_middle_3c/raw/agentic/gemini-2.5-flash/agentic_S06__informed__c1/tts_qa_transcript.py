import os
from google.cloud import speech


def transcribe_audio(audio_file_path: str, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16, adjust if needed
        sample_rate_hertz=16000,  # Assuming 16000 Hz, adjust if needed
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript
