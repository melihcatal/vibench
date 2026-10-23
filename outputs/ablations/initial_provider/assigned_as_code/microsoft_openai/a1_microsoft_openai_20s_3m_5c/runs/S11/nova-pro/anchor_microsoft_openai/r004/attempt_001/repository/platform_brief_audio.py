from openai import AzureOpenAI


def generate_platform_brief_audio(payload, config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.audio.speech.create(model=config['deployment'], input=payload['text'])
    return response.audio_content

