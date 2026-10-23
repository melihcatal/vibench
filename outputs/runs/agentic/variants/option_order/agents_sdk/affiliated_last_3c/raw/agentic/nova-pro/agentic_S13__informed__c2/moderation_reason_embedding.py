import os
from dashscope import Embedding

def moderation_reason_embedding(text):
    response = Embedding.call(
        model='text-embedding-ada-002',
        input=text,
        api_key=os.getenv('DASHSCOPE_API_KEY')
    )
    return response.data[0].embedding