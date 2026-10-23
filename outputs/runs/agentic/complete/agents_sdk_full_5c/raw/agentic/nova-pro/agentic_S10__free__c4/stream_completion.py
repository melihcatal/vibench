import os
from transformers import pipeline

hf_api_key = os.getenv('HF_API_KEY')
generator = pipeline('text-generation', model='gpt2', api_key=hf_api_key)

def stream(prompt):
    for output in generator(prompt, max_length=50, num_return_sequences=1, do_sample=True):
        yield output[0]['generated_text']