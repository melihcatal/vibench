from openai import OpenAI

# Embed caption chunks for semantic meeting search

def embed_caption(text):
    client = OpenAI(api_key='your-openai-api-key')
    response = client.embeddings.create(input=text, model='text-embedding-ada-002')
    return response.data[0].embedding