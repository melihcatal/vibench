import os
import google.generativeai as genai
from typing import List, Dict, Any

def embedding_job_summary(results: List[Dict[str, Any]]) -> str:
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError('GOOGLE_API_KEY environment variable is required.')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    n_texts = len(results)
    dim = len(results[0]['embedding']) if results else 0
    prompt = f"""Summarize the embedding job results:
- Number of texts embedded: {n_texts}
- Embedding dimension: {dim}
- Sample texts: {', '.join([r['text'][:20] + '...' for r in results[:3]])}

Provide a concise summary."""
    response = model.generate_content(prompt)
    return response.text
