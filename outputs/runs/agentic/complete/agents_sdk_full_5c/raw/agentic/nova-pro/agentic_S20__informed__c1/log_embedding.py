import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.embeddings.create(
    model='text-embedding-ada-002',
    input=['Sample log message']
)

print(response.data[0].embedding)