import os
from typing import List, Dict
import openai

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def summarize_transcript(transcript_text: str, model_name: str = "gpt-3.5-turbo") -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = OPENAI_API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
        {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
    ]

    response = openai.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()