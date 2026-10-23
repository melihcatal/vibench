import os
from typing import List
from security_client import SecurityClients
from security_models import EmbeddingResult

def embed_audit_notes(notes_text: str, model: str = "text-embedding-ada-002") -> EmbeddingResult:
    client = SecurityClients.get_openai_client()
    try:
        response = client.embeddings.create(
            input=notes_text,
            model=model
        )
        embedding_vector = response.data[0].embedding
        return EmbeddingResult(original_text=notes_text, embedding=embedding_vector)
    except Exception as e:
        raise RuntimeError(f"Error generating embedding for audit notes with OpenAI: {e}")

def embed_multiple_audit_notes(notes_list: List[str], model: str = "text-embedding-ada-002") -> List[EmbeddingResult]:
    client = SecurityClients.get_openai_client()
    try:
        response = client.embeddings.create(
            input=notes_list,
            model=model
        )
        results = []
        for i, data_item in enumerate(response.data):
            results.append(EmbeddingResult(original_text=notes_list[i], embedding=data_item.embedding))
        return results
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings for multiple audit notes with OpenAI: {e}")