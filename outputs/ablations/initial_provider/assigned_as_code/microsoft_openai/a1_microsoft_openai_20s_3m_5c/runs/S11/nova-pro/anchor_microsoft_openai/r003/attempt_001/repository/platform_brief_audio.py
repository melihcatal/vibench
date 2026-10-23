from openai import AzureOpenAI
from model_client import get_model_client



def generate_platform_brief_audio(output, config):
    client = get_model_client(config)
    response = client.audio.speech.create(model='tts-1', input=output['text'])
    return {'audio': response.content}