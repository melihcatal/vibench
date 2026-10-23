import os

import openai

def extract_json(text: str) -> dict:
    """Extract structured JSON from text using a hosted LLM."""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Extract JSON from the following text: {text}",
        max_tokens=150,
        temperature=0.7,
    )
    extracted_json = response.choices[0].text.strip()
    return eval(extracted_json)
