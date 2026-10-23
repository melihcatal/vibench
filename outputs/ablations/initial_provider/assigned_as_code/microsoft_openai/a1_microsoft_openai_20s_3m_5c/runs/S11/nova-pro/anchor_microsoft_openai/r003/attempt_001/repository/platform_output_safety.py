from openai import AzureOpenAI
from model_client import get_model_client



def check_platform_output_safety(output, config):
    client = get_model_client(config)
    response = client.moderations.create(input=output['text'])
    return response.results[0].flagged