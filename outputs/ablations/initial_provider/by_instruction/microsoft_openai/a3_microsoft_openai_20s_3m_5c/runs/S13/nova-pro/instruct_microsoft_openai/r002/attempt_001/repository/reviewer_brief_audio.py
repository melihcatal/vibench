import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15'
)

def generate_brief(text):
    response = client.audio.speech.create(
        input=text,
        model='text-to-speech-stable'
    )
    return response.audio_content