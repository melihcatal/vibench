import os
from google.cloud import speech_v1p1beta1 as speech


def transcribe_synthesized_qa(gcs_uri: str, language_code: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    The audio file must be stored in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming common WAV format for QA
        sample_rate_hertz=16000,  # Adjust if your audio has a different sample rate
        language_code=language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)  # Adjust timeout as needed

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()
