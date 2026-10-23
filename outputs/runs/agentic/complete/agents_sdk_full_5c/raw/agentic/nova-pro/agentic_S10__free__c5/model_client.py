import os
from transformers import pipeline

def get_pipeline(task, model_name):
    return pipeline(task, model=model_name)

def configure(model_name):
    os.environ['TRANSFORMERS_CACHE'] = 'path_to_cache'