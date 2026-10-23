from model_client import client
from model_models import ModelRequest, normalize_response

def embed_output(text):
    request = ModelRequest(f'Embed the following text: {text}')
    response = client.embeddings.create(
        input=[text],
        model='text-embedding-ada-002'
    )
    return response.data[0].embedding