import os
from typing import List, Dict, Optional
from openai import OpenAI
from embeddings_models import EmbeddingResponse, BatchEmbeddingResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GPT_MODEL = "gpt-4o-mini"


def summarize_embedding_job(
    texts: List[str],
    embeddings_result: BatchEmbeddingResponse,
    model: str = GPT_MODEL,
    api_key: Optional[str] = None,
) -> str:
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=key)
    text_preview = "\n".join(f"- {t[:120]}" for t in texts[:10])
    if len(texts) > 10:
        text_preview += f"\n... and {len(texts) - 10} more texts"
    prompt = (
        f"Summarize the following embedding job results:\n\n"
        f"Model used: {embeddings_result.models[0] if embeddings_result.models else 'unknown'}\n"
        f"Total texts embedded: {len(texts)}\n"
        f"Embedding dimension: {embeddings_result.dimension}\n"
        f"Total tokens used: {embeddings_result.usage_tokens}\n\n"
        f"Sample texts:\n{text_preview}\n\n"
        f"Provide a concise summary of the embedding job including model details, "
        f"dimensionality, token usage efficiency, and the nature of the embedded content."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an embedding job analyst. Provide concise summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def generate_embedding_report(
    texts: List[str],
    embeddings_result: BatchEmbeddingResponse,
    model: str = GPT_MODEL,
    api_key: Optional[str] = None,
) -> Dict:
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=key)
    avg_dim = embeddings_result.dimension
    avg_tokens = embeddings_result.usage_tokens / max(len(texts), 1)
    prompt = (
        f"Generate a structured JSON report for this embedding job:\n"
        f"- Total documents: {len(texts)}\n"
        f"- Embedding model: {embeddings_result.models[0] if embeddings_result.models else 'unknown'}\n"
        f"- Vector dimensions: {avg_dim}\n"
        f"- Average tokens per document: {avg_tokens:.1f}\n"
        f"- Total tokens consumed: {embeddings_result.usage_tokens}\n\n"
        f"Return a JSON object with keys: summary, model_info, statistics, recommendations."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an embedding job analyst. Return valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    return {"report": response.choices[0].message.content.strip()}
