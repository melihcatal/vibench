import os
from typing import List, Dict, Any
from openai import OpenAI


def embedding_job_summary(
    texts: List[str], embeddings: List[List[float]], model: str = "gpt-4o-mini"
) -> str:
    """
    Summarize embedding job results using OpenAI's chat completion API.

    Args:
        texts: List of original texts that were embedded
        embeddings: List of embedding vectors
        model: OpenAI model to use for summarization (default: gpt-4o-mini)

    Returns:
        Summary of the embedding job
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    text_samples = texts[:5] if len(texts) > 5 else texts
    embedding_dims = len(embeddings[0]) if embeddings else 0

    prompt = f"""
    Summarize this embedding job:
    - Number of texts processed: {len(texts)}
    - Embedding dimensions: {embedding_dims}
    - Sample texts: {text_samples}
    
    Provide a brief summary including:
    1. Overall characteristics of the text corpus
    2. Any patterns or themes in the sample texts
    3. Potential use cases for these embeddings
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes embedding job results.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content
