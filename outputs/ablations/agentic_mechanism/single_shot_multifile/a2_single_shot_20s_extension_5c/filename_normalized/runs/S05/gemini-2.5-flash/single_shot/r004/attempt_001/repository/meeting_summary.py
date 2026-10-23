import os
from typing import Dict, Any
import openai

def summarize_text(text_chunk: str, model: str = "gpt-4o") -> str:
    """Summarizes a chunk of meeting transcript text using OpenAI Chat Completions API.

    Args:
        text_chunk: The text content from the meeting to summarize.
        model: The OpenAI model to use for summarization (e.g., "gpt-3.5-turbo", "gpt-4o").

    Returns:
        str: A concise summary of the text chunk.
    """
    if not text_chunk.strip():
        return ""

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts. Provide a concise summary."},
                {"role": "user", "content": f"Please summarize the following meeting segment: {text_chunk}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI summarization error: {e}")
        return "Failed to summarize."
