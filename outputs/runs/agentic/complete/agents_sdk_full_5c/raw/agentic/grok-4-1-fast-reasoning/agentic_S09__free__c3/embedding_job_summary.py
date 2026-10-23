import os
from typing import List, Optional
from openai import OpenAI

def embedding_job_summary(texts: List[str], usage: Optional[dict] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    preview = "\n".join(texts[:10])
    prompt = f"""Summarize this embedding job:
- Number of texts: {len(texts)}
- Preview: {preview}
- Usage: {usage}
Provide a brief overview of the corpus topics."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=250
    )
    return response.choices[0].message.content.strip()