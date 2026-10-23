import openai

openai.api_key = 'your-api-key'

response = openai.Embedding.create(
    input='Hello, world!',
    model='text-embedding-ada-002'
)

print(response['data'][0]['embedding'])
