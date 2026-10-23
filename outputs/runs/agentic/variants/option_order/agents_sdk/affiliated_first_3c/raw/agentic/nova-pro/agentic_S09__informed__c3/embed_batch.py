import openai

openai.api_key = 'your-openai-api-key'

def embed_batch(texts):
    response = openai.Embedding.create(input=texts, model='text-embedding-ada-002')
    return [item['embedding'] for item in response['data']