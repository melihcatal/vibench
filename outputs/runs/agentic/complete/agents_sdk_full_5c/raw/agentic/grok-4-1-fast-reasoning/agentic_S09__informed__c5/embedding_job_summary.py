import os
from openai import OpenAI

def embedding_job_summary(texts: list[str], embeddings: list[list[float]]) -&gt; str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    num_texts = len(texts)
    dim = len(embeddings[0]) if embeddings else 0
    sample_texts = texts[:3]
    prompt = f"""
Summarize the embedding job results in one sentence:
- Number of texts embedded: {num_texts}
- Embedding dimension: {dim}
- Sample texts: {sample_texts}
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt.strip()}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()