import os
import json
from dashscope import tts
from dashscope.tts import TextToSpeechOptions

# Load credentials from environment
API_KEY = os.getenv("DASHSCOPE_API_KEY")
assert API_KEY, "Set DASHSCOPE_API_KEY environment variable"


def synthesize_plain_text(text: str, voice: str = "default") -> bytes:
    """Synthesize plain text to an audio byte stream using DashScope CosyVoice.
    Returns the raw audio bytes.
    """
    client = tts.Client(api_key=API_KEY)
    options = TextToSpeechOptions(
        model="cosyvoice",
        voice=voice,
        format="wav",
    )
    response = client.text_to_speech(text, options=options)
    return response.audio_bytes


def synthesize_ssml(ssml: str, voice: str = "default") -> bytes:
    """Synthesize SSML with voice and prosody controls.
    Returns raw audio bytes.
    """
    client = tts.Client(api_key=API_KEY)
    options = TextToSpeechOptions(
        model="cosyvoice",
        voice=voice,
        format="wav",
        ssml=True,
    )
    response = client.text_to_speech(ssml, options=options)
    return response.audio_bytes
