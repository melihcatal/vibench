from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

def transcribe_audio(audio_file_path: str, sample_rate_hertz: int, language_code: str = "en-US"):
    """
    Transcribes audio from a local file using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The path to the audio file.
        sample_rate_hertz: The sample rate of the audio file in Hertz.
        language_code: The language code of the audio (e.g., "en-US", "es-ES").

    Returns:
        A string containing the transcribed text.
    """
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()

