import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_brief_audio(text):
    response = openai.Audio.create(input=text, voice='alloy', model='tts-1')
    return response.audio_url