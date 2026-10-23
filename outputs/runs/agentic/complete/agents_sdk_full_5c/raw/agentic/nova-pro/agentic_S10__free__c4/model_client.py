import os
from transformers import pipeline

def get_pipeline(task, model):
    hf_api_key = os.getenv('HF_API_KEY')
    return pipeline(task, model=model, api_key=hf_api_key)