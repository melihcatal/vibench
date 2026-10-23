# synthesize_text.py
import dashscope

# DashScope API key should be set in environment variable DASHSCOPE_API_KEY


def synthesize_text(text: str, voice: str = "default") -> bytes:
    """Synthesize plain text to an audio byte stream using DashScope CosyVoice.

    Args:
        text: The plain text to synthesize.
        voice: Identifier for the voice to use.

    Returns:
        Binary audio data.
    """
    client = dashscope.TextToSpeech()
    response = client.synthesize(text=text, voice=voice, format="wav")
    return response.audio_bytes
