import os
from dashscope import Generation

api_key = os.getenv('DASHSCOPE_API_KEY')

def summarize_audit_events(events):
    response = Generation.call('qwen-turbo', prompt=f'Summarize the following audit events: {events}', api_key=api_key)
    return response.output.choices[0].message.content