import os
import json
import pytest
from typing import Any

# Reference: DashScope embeddings (text embeddings) for fast similarity search
# Provider identifier: dashscope SDK
from dashscope import text_embeddings
from dashscope.embeddings import EmbeddingRequest

# Environment variables used by dashscope (API key is required)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError("Set DASHSCOPE_API_KEY environment variable before running tests")


def generate_qa_embedding(question: str) -> Any:
    """Create an embedding for a QA sample using DashScope.

    Identifies provider via `dashscope` import and uses `DASHSCOPE_API_KEY`.
    """
    response = text_embeddings.embeddings(
        texts=[question],
        model="qwen2.5-72k-pro",
    )
    # response shape: {"embeddings": [[...]]}
    return response["embeddings"][0]

@embed_qa_samples = generate_qa_embedding

def test_qa_transcription(transcribed_text: str, expected_embeddings: List[float]) -> None:
    """Integration test that (1) embeds the synthesized QA output and (2) compares
    it to a stored embedding vector.  The test uses pytest and asserts cosine
    similarity > 0.85 as a proxy for correct spoken content.
    """
    synthesized_embedding = generate_qa_embedding(transcribed_text)
    # Simple cosine similarity check (pseudo implementation)
    from math import sqrt
    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = sqrt(sum(x * x for x in a))
        mag_b = sqrt(sum(y * y for y in b))
        return dot / (mag_a * mag_b)
    similarity = cosine(expected_embeddings, synthesized_embedding)
    assert similarity > 0.85, "QA transcription does not match expected spoken content"

# Example placeholder for CI / local run
if __name__ == "__main__":
    pytest.main([__file__])
