import os
from dashscope import Generation

def moderation_summary(text):
    response = Generation.call(
        model='qwen-turbo',
        messages=[{
            'role': 'user',
            'content': f'Summarize the following text: {text}'
        }],
        api_key=os.getenv('DASHSCOPE_API_KEY')
    )
    return response.output.choices[0].message.content