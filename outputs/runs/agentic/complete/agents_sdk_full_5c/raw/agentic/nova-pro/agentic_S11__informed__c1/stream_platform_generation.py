import os
from dashscope import Generation

api_key = os.getenv('DASHSCOPE_API_KEY')

response = Generation.call(
    model='text-davinci-003',
    prompt='Hello, world!',
    api_key=api_key,
    stream=True
)
for chunk in response:
    print(chunk, end='')