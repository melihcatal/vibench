import os
from openai import OpenAI

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (OpenAI's GPT-3.5 Turbo) to summarize long text.
    """
    # Initialize OpenAI client
    # Ensure OPENAI_API_KEY environment variable is set
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Please summarize the following text:

{text}"}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

