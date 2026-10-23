import os
import speech_client


def synthesize_text(text: str) -> bytes:
    """Synthesize plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text (str): The plain text to synthesize.

    Returns:
        bytes: The synthesized audio as an MP3 byte stream.
    """
    client = speech_client.TextToSpeechClient()
    # Build the request
    request = {
        "input": {
            "text": text,
        },
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Wavenet-D",  # concrete provider voice
        },
        "audioConfig": {
            "audioEncoding": "MP3",
        },
    }
    # Call the provider API
    response = client.synthesize_speech(request)
    # response['audio_content'] is a byte string
    return response["audio_content"]
