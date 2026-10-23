import os
from openai import OpenAI

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using a hosted OpenAI LLM.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION"),
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another suitable OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
