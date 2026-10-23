from openai import OpenAI

OPENAI_API_KEY = 'your_openai_api_key'

def embed_moderation_reason(reason):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(input=reason, model='text-embedding-3-large')
    return response.data[0].embedding