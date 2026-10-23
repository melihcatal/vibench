import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def generate_spoken_brief(text):
    response = client.speech.create(
        model='tts-001',
        input=text
    )
    return response.audio_content