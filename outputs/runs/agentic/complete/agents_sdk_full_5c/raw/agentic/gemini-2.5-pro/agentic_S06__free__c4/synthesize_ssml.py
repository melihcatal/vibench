"""
Uses Amazon Polly to synthesize SSML with voice and prosody controls.
"""
import boto3
from speech_client import get_polly_client

def synthesize_polly_ssml(ssml_text: str, voice_id: str = "Joanna") -> bytes:
    """
    Synthesizes SSML text into speech using Amazon Polly.

    Args:
        ssml_text: The SSML text to synthesize.
        voice_id: The ID of the Polly voice to use.

    Returns:
        The audio content as a byte stream (MP3).
    """
    client = get_polly_client()

    response = client.synthesize_speech(
        Text=ssml_text,
        TextType="ssml",
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine="neural"
    )

    audio_stream = response.get("AudioStream")
    if audio_stream:
        return audio_stream.read()
    else:
        raise IOError("Could not get audio stream from Polly response.")
