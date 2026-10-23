import os
import dashscope

def get_client():
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    return dashscope

def get_model(model_name):
    return model_name