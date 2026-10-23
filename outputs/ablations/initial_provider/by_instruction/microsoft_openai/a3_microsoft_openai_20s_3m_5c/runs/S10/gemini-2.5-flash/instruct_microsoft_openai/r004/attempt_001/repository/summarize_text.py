import os
from openai import OpenAI

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (OpenAI) to summarize long text.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    response = client.chat.completions.create(
        model="gpt-4o", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content