import openai

def embed_text(text):
    openai.api_key = 'your-api-key'
    response = openai.Embedding.create(input=text)
    return response['data'][0]['embedding']