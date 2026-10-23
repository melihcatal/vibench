from typing import List
import google.generativeai as genai
from model_client import get_model_client


def embed_text(text: str) -> List[float]:
    """
    Embeds a single piece of text.
    """
    result = genai.embed_content(
        model="models/text-embedding-004", content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]


def embed_text_batch(texts: List[str]) -> List[List[float]]:
    """
    Embeds a batch of texts.
    """
    result = genai.embed_content(
        model="models/text-embedding-004", content=texts, task_type="RETRIEVAL_DOCUMENT"
    )
    return [embedding for embedding in result["embedding"]]
