import os
from dashscope import Generation

def summarize_quality_issues(text):
    response = Generation.call('qwen-turbo', messages=[{'role': 'user', 'content': text}])
    return response.output.choices[0].message.content