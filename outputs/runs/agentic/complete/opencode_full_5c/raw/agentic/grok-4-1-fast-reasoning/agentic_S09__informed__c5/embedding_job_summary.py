import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embedding_job_summary(results: List[Dict[str, Any]]) -> str:
    texts = [result.get("text", "")[:200] + "..." for result in results]
    prompt = f"""Summarize this embedding job:

- Number of embeddings generated: {len(results)}
- Sample texts: {"; ".join(texts[:5])}

Provide key insights about the corpus content and any patterns."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content
