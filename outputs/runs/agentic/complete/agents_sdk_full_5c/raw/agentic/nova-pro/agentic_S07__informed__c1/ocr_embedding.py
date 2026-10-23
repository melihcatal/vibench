from openai import OpenAI

def embed_text(text):
    client = OpenAI(api_key='your-api-key')
    response = client.embeddings.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']