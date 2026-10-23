import os
from transformers import pipeline

hf_api_key = os.getenv('HF_API_KEY')
extractor = pipeline('text2text-generation', model='t5-base', api_key=hf_api_key)

def extract(text):
    return extractor(text, max_length=130, min_length=30, do_sample=False)[0]['generated_text']