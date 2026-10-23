import os
from dashscope import Generation

os.environ['DASHSCOPE_API_KEY'] = 'your-dashscope-api-key'

def embed_script(text):
    response = Generation.call(model='qwen-turbo', prompt=text)
    return response['output']['text']