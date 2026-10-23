import openai

def embed_crypto_audit_notes(text):
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']