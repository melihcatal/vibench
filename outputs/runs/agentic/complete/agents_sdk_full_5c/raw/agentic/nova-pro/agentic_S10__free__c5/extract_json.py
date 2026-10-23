import os
from transformers import pipeline

model_name = 'distilbert-base-uncased'
extractor = pipeline('text2json', model=model_name)

def extract(text):
    return extractor(text)[0]