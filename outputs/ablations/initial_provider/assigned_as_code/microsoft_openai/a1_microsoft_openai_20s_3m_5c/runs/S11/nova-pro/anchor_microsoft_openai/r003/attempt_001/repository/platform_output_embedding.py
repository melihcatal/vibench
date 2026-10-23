from openai import AzureOpenAI
from model_client import get_model_client



def embed_platform_output(output, config):
    client = get_model_client(config)
    response = client.embeddings.create(model='text-embedding-ada-002', input=output['text'])
    return {'embedding': response.data[0].embedding}