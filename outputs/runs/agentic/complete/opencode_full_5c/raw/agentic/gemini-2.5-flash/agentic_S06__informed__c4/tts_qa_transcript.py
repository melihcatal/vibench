import os
from google.cloud import speech


def transcribe_audio(audio_file_path: str) -> str:
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Assuming MP3 for synthesized audio
        sample_rate_hertz=16000,  # Adjust if your TTS output is different
        language_code="en-US",  # Adjust based on your synthesis language
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()
