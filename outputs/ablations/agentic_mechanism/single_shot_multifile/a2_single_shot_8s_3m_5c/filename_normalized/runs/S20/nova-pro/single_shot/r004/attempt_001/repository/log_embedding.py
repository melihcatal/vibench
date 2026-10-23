import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

log_message = 'User login failed due to invalid credentials'
embedding = openai.Embedding.create(
    input=log_message,
    model='text-embedding-ada-002'
)
print(embedding['data'][0]['embedding'])
