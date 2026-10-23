from typing import List, Optional
import numpy as np
from embeddings_client import get_embeddings_client

LLM_MODEL = "gpt-4o-mini"

def embedding_job_summary(embeddings: List[List[float]], texts: Optional[List[str]] = None) -> str:
    client = get_embeddings_client()
    if not embeddings:
        return "No embeddings provided."
    num_embs = len(embeddings)
    dim = len(embeddings[0])
    norms = [np.linalg.norm(np.array(e)) for e in embeddings]
    avg_norm = np.mean(norms)
    stats = f"Number of embeddings: {num_embs}\nDimension: {dim}\nAvg norm: {avg_norm:.2f}"
    if texts:
        lengths = [len(t) for t in texts]
        avg_len = np.mean(lengths)
        stats += f"\nAvg text length: {avg_len:.0f} chars"
    prompt = f"Summarize this embedding job:\n\n{stats}\n\nProvide a brief professional summary."
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()