from openai import AzureOpenAI
from model_client import get_model_client



def translate_platform_output(output, target_language, config):
    client = get_model_client(config)
    response = client.translations.create(model='text-translation', input=output['text'], to=target_language)
    return {'text': response.text}