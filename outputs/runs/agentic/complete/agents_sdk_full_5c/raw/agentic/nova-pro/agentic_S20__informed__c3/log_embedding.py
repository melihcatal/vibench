import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

model = 'text-embedding-ada-002'

text = 'log message to embed'

response = openai.Embedding.create(input=text, model=model)