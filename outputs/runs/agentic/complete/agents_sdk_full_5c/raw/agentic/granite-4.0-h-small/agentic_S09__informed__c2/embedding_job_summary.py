import os
import math
from typing import List

# DashScope client for hosted LLM inference
import dashscope

dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
if not dashscope.api_key:
    raise RuntimeError('Set DASHSCOPE_API_KEY environment variable')

DEFAULT_MODEL = 'qwen-embedding-v1'  # DashScope Qwen embedding model

def summarize_embedding_job(results: List[dict]) -> str:
    """Create a concise summary of an embedding job's results.

    Args:
        results: List of raw responses from the LLM service.
    Returns:
        Human‑readable summary string.
    """
    n_success = sum(1 for r in results if isinstance(r, dict) and 'embedding' in r)
    n_failed = len(results) - n_success
    return f'Embedding job completed: {n_success} successes, {n_failed} failures'


def check_corpus_safety(text: str) -> bool:
    """Very simple safety filter (placeholder). Returns True for demo.

    In a production system replace with a call to a content‑safety API.
    """
    # Placeholder: allow any non‑empty string
    return bool(text.strip())


def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a query to the target language before multilingual search.

    Uses DashScope translation endpoint (placeholder implementation).
    """
    # Placeholder: return the original text if target_lang is 'en'
    return query


def generate_audio_brief(transcripts: List[str]) -> str:
    """Create a spoken‑brief from retrieved search results.

    Concatenates summaries of each transcript.
    """
    brief_parts = [f'Summary: {t[:60]}...' for t in transcripts]
    return ' | '.join(brief_parts)
