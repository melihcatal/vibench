import os
from dashscope import Embedding

def embed_text(text):
    response = Embedding.create_embedding(
        api_key=os.environ.get('DASHSCOPE_API_KEY'),
        model='text-embedding-ada-002',
        input=text
    )
    return response['data'][0]['embedding']