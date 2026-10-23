from openai import OpenAI
import os

def summarize_record(text: str, model: str = "gpt-4o-mini") -> str:
    """
    Summarizes a document record using OpenAI's GPT model.
    
    Args:
        text: The text content to summarize.
        model: The OpenAI model identifier.
        
    Returns:
        str: The generated summary.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the following text:"},
            {"role": "user", "content": text}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()