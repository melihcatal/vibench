import os
import openai

def transcript_embedding(transcript):
    api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_key = api_key
    response = openai.Embedding.create(
        input=transcript,
        model='text-embedding-ada-002'
    )
    return response['data'][0]['embedding']