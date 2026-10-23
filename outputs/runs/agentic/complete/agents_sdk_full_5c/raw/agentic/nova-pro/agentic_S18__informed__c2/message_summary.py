import os
from dashscope import Generation
os.environ['DASHSCOPE_API_KEY'] = 'your_api_key'

def summarize(text):
    response = Generation.call('qwen-turbo', prompt=text, top_p=0.8, temperature=0.95)
    return response.output.choices[0].text