import os
from transformers import pipeline

hf_api_key = os.getenv('HF_API_KEY')
answerer = pipeline('question-answering', model='distilbert-base-cased-distilled-squad', api_key=hf_api_key)

def answer(question, context):
    return answerer(question=question, context=context)[0]['answer']