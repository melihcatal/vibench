import os
from dashscope import TextToSpeech


def synthesize_ssml(ssml):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    response = TextToSpeech.synthesis(
        ssml=ssml, voice="en-US-Wavenet-D", api_key=api_key
    )
    return response.audio_content
