import os
from dashscope import Generation

def select_resource():
    api_key = os.getenv('DASHSCOPE_API_KEY')
    generation = Generation(api_key=api_key)
    models = generation.list_models()
    return models