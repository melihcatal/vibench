import os
import dashscope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def spoken_brief(text):
    """Generate a spoken brief (audio) from text using TTS."""
    client = dashscope.TextToSpeech(api_key=DASHSCOPE_API_KEY, model="cosyvoice")
    response = client.synthesize(text=text, voice="en-US-Wavenet-D")
    # response contains audio bytes
    return response.audio_bytes
