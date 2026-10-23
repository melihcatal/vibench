import json
import os
from openai import OpenAI


def summarize_asset(text: str, model="gpt-4o-mini") -> str:
    """Summarize extracted content using an OpenAI hosted LLM.

    Provider: OpenAI Chat Completion (openai SDK).
    API key is read from OPENAI_API_KEY environment variable.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following content in 2-3 concise sentences:\n\n{text}",
                }
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Summarization failed: {e}")

    print("Asset summarization completed using OpenAI model")
