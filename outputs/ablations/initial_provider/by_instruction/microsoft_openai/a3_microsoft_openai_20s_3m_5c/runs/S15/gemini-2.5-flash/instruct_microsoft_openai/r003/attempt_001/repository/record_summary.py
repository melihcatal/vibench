import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

def summarize_record(record_content: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes document records concisely."}, 
            {"role": "user", "content": f"Please summarize the following document record:\n\n{record_content}"}
        ]
    )
    
    return response.choices[0].message.content.strip()
