import os
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio

def transcribe_audio_from_file(file_path: str, language_code: str = "en-US") -> str:
    """
    Transcribes an audio file (e.g., a synthesized QA sample) using Google Cloud Speech-to-Text.
    """
    client: SpeechClient = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = RecognitionAudio(content=content)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 from TTS output
        sample_rate_hertz=16000, # Common sample rate, adjust if TTS output differs
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return transcript.strip()
