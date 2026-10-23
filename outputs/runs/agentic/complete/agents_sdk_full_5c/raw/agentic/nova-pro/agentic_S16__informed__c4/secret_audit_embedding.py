import openai

def secret_audit_embedding(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Embedding.create(input=text, engine='text-embedding-ada-002')
    return response['data'][0]['embedding']