import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def embed_log_message(text):
    response = openai.Embedding.create(
        input=text,
        model='text-embedding-ada-002'
    )
    return response['data'][0]['embedding']