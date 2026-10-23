# timestamped_transcript.py
import os
import requests

# Provider: IBM Watson Speech to Text (provider identifiable via API key and URL)
import ibm_watson


def timestamped_transcript(audio_path):
    """Return word or segment timestamps from a transcription result.

    Returns a list of timestamped words.
    """
    service = ibm_watson.speech_to_text_v1.SpeechToTextV1(
        authenticator=ibm_watson.IamAuthenticator(os.getenv("IBM_API_KEY"))
    )
    service.set_service_url(os.getenv("IBM_URL"))
    with open(audio_path, "rb") as audio_file:
        result = service.recognize(
            audio=audio_file, content_type="audio/wav", timestamps=True
        ).get_result()
    return result["results"][0]["alternatives"][0]["timestamps"]
