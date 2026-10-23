import os
from transformers import pipeline

model_name = 'distilbert-base-uncased'
summarizer = pipeline('summarization', model=model_name)

def summarize(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']