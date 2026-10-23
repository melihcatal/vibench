import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_audio_brief(text):
    response = openai.Audio.create(input=text, model='tts-001')
    return response['audio_url']