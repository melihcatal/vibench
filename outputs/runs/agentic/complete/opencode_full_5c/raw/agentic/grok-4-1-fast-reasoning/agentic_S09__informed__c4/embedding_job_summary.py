import os
import google.generativeai as genai
from typing import List


def embedding_job_summary(embeddings: List[List[float]], texts: List[str]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    num_texts = len(texts)
    dim = len(embeddings[0]) if embeddings else 0
    norms = [sum(e**2 for e in emb) ** 0.5 for emb in embeddings]
    avg_norm = sum(norms) / num_texts if num_texts else 0

    prompt = f"""Summarize this embedding job results concisely:
- Processed {num_texts} texts
- Dimension: {dim}
- Average L2 norm: {avg_norm:.4f}
Sample texts (first 3): {texts[:3]}
"""

    response = model.generate_content(prompt)
    return response.text
