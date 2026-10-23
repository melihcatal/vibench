import os

def get_api_key(service):
    return os.getenv(f'{service}_API_KEY')

def create_client(service):
    if service == 'bedrock':
        import boto3
        return boto3.client('bedrock-runtime')
    elif service == 'mistral':
        from mistralai.client import MistralClient
        return MistralClient(api_key=get_api_key('MISTRAL'))
    elif service == 'openai':
        import openai
        openai.api_key = get_api_key('OPENAI')
        return openai
    elif service == 'anthropic':
        from anthropic import Anthropic
        return Anthropic(api_key=get_api_key('ANTHROPIC'))