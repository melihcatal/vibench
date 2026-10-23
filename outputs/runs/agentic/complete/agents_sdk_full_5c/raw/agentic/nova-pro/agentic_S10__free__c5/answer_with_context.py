import os
from transformers import pipeline

model_name = 'distilbert-base-uncased'
qa_pipeline = pipeline('question-answering', model=model_name)

def answer(question, context):
    return qa_pipeline(question=question, context=context)