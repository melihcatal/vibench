import os
from dashscope import Generation

def generate_quality_summary(text):
    api_key = os.getenv('DASHSCOPE_API_KEY')
    response = Generation.call(model='qwen-turbo', prompt=text, api_key=api_key)
    return response.output.choices[0].message.content