import os
from typing import Tuple, Dict

# Concrete LLM summarization provider: OpenAI ChatGPT (hosted API)
import openai
from openai.error import OpenAIError

def summarize_asset(plain_text: str, summary_length: int = 150) -> str:
    """Generate a concise summary of asset text using OpenAI GPT model.",
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')  # ensure provider credential is set
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': f\"Summarize the following text in {summary_length} words:\\n\\n{plain_text}\"}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")
