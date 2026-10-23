import os
from transformers import pipeline

model_name = 'distilbert-base-uncased'
text_generator = pipeline('text-generation', model=model_name)

def stream(prompt):
    for output in text_generator(prompt, max_length=50, num_return_sequences=1, pad_token_id=50256):
        yield output[0]['generated_text']