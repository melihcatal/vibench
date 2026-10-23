import os
from transformers import pipeline

hf_api_key = os.getenv('HF_API_KEY')
summarizer = pipeline('summarization', model='t5-base', api_key=hf_api_key)

def summarize(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']