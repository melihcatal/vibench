# synthesize_ssml.py
import dashscope

# DashScope API key should be set in environment variable DASHSCOPE_API_KEY


def synthesize_ssml(ssml: str, voice: str = "default", prosody: dict = None) -> bytes:
    """Synthesize SSML to an audio byte stream using DashScope CosyVoice with optional prosody controls.

    Args:
        ssml: The SSML markup to synthesize.
        voice: Voice identifier.
        prosody: Optional dict containing 'rate', 'pitch', 'volume' adjustments.

    Returns:
        Binary audio data.
    """
    client = dashscope.TextToSpeech()
    payload = {"ssml": ssml, "voice": voice, "format": "wav"}
    if prosody:
        payload["prosody"] = prosody
    response = client.synthesize(**payload)
    return response.audio_bytes
