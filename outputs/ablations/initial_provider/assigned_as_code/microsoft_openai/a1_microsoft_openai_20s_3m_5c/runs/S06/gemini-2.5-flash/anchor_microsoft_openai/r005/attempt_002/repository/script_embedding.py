from openai import OpenAI
import os


def script_embedding(payload, config=None):
    config = config or {}
    
    # os.environ['OPENAI_API_KEY'] = config['openai_api_key']
    client = OpenAI(api_key=config['openai_api_key'])
    
    text_to_embed = payload['text']
    model = payload.get('model', 'text-embedding-ada-002')
    
    response = client.embeddings.create(input=text_to_embed, model=model)
    
    return {'embedding': response.data[0].embedding, 'model': model}