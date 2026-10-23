import os
import speech_client


def synthesize_ssml(ssml: str) -> bytes:
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml (str): The SSML markup to synthesize.

    Returns:
        bytes: The synthesized audio as an MP3 byte stream.
    """
    client = speech_client.TextToSpeechClient()
    request = {
        "input": {
            "ssml": ssml,
        },
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Wavenet-D",  # concrete provider voice
        },
        "audioConfig": {
            "audioEncoding": "MP3",
        },
    }
    response = client.synthesize_speech(request)
    return response["audio_content"]
