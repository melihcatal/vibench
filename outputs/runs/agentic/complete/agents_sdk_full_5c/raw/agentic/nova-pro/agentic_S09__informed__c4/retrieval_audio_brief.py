import os
from dashscope import Text2Speech

def generate_audio_brief(text):
    response = Text2Speech.synthesis(text=text, voice='en-US', model='cosyvoice', api_key=os.getenv('DASHSCOPE_API_KEY'))
    return response.audio_content