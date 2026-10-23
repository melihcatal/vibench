import os
from dashscope import TextToSpeech

api_key = os.getenv("DASHSCOPE_API_KEY")


def generate_spoken_brief(text):
    response = TextToSpeech.synthesis(model="cosyvoice", text=text, api_key=api_key)
    return response
