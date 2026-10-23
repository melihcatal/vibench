import google.generativeai as genai
import os
from typing import List
from security_models import EmbeddingResult
from security_client import get_gemini_api_key

def embed_audit_note(text: str) -> EmbeddingResult:
    """
    Generates an embedding for a crypto audit note using Google Gemini Embeddings.

    Args:
        text: The audit note text to embed.

    Returns:
        An EmbeddingResult object containing the original text and its embedding.
    """
    genai.configure(api_key=get_gemini_api_key())

    # The 'embedding-001' model is a common choice for general text embeddings.
    # Check the latest available models if this one changes.
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    
    # The embedding is usually a list of floats.
    embedding = response['embedding']
    return EmbeddingResult(text=text, embedding=embedding)

def embed_multiple_audit_notes(texts: List[str]) -> List[EmbeddingResult]:
    """
    Generates embeddings for multiple crypto audit notes in a batch.

    Args:
        texts: A list of audit note texts to embed.

    Returns:
        A list of EmbeddingResult objects.
    """
    genai.configure(api_key=get_gemini_api_key())

    response = genai.embed_content(
        model="models/embedding-001",
        content=texts
    )

    results = []
    for i, embedding in enumerate(response['embedding']):
        results.append(EmbeddingResult(text=texts[i], embedding=embedding))
    return results

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY)
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

    # audit_note_1 = "Successful key rotation event for production database encryption key."
    # audit_note_2 = "Failed decryption attempt from unauthorized IP 192.168.1.100."
    # audit_note_3 = "Compliance review of key access policies completed, no issues found."

    # print(f"Embedding audit note: '{audit_note_1}'")
    # try:
    #     embedding_result_1 = embed_audit_note(audit_note_1)
    #     print(f"  Embedding length: {len(embedding_result_1.embedding)}")
    #     print(f"  First 5 dimensions: {embedding_result_1.embedding[:5]}")
    # except Exception as e:
    #     print(f"Error embedding note 1: {e}")
    # print("-" * 30)

    # audit_notes = [audit_note_1, audit_note_2, audit_note_3]
    # print("Embedding multiple audit notes:")
    # try:
    #     embedding_results = embed_multiple_audit_notes(audit_notes)
    #     for i, res in enumerate(embedding_results):
    #         print(f"Note {i+1} ('{res.text[:50]}...'): Embedding length {len(res.embedding)}")
    #         print(f"  First 5 dimensions: {res.embedding[:5]}")
    # except Exception as e:
    #     print(f"Error embedding multiple notes: {e}")
