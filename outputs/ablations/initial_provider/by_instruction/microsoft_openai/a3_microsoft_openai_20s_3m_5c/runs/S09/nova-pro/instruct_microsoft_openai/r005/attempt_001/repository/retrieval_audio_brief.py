import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def generate_spoken_brief(text: str) -> str:
    response = client.speech.create(
        input=text,
        voice='en-US-GuyNeural',
        model='text-to-speech-api-001'
    )
    return response.audio_url