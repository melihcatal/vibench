import cohere
import os
import numpy as np
from typing import Dict, Any, List, Optional, Union


class CohereEmbedder:
    """Embedder using Cohere Embed API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(self.api_key)

    def embed_text(
        self,
        text: str,
        model: str = "embed-english-v3.0",
        input_type: str = "search_document",
        truncate: str = "END",
    ) -> Dict[str, Any]:
        """
        Generate embeddings for text using Cohere API.
        """
        try:
            response = self.client.embed(
                texts=[text], model=model, input_type=input_type, truncate=truncate
            )

            embedding = response.embeddings[0]

            return {
                "text": text,
                "embedding": embedding,
                "embedding_dimension": len(embedding),
                "model": model,
                "input_type": input_type,
                "provider": "cohere",
                "metadata": {
                    "response_id": response.response_id,
                    "token_count": getattr(response, "token_count", None),
                },
            }

        except Exception as e:
            return {"text": text, "error": str(e), "model": model, "provider": "cohere"}

    def embed_batch(
        self,
        texts: List[str],
        model: str = "embed-english-v3.0",
        input_type: str = "search_document",
        truncate: str = "END",
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for multiple texts.
        """
        try:
            response = self.client.embed(
                texts=texts, model=model, input_type=input_type, truncate=truncate
            )

            results = []
            for i, (text, embedding) in enumerate(zip(texts, response.embeddings)):
                results.append(
                    {
                        "text": text,
                        "embedding": embedding,
                        "embedding_dimension": len(embedding),
                        "model": model,
                        "input_type": input_type,
                        "provider": "cohere",
                        "metadata": {
                            "response_id": response.response_id,
                            "token_count": getattr(response, "token_count", None),
                            "index": i,
                        },
                    }
                )

            return results

        except Exception as e:
            return [
                {"text": text, "error": str(e), "model": model, "provider": "cohere"}
                for text in texts
            ]

    def similarity_search(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        model: str = "embed-english-v3.0",
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search between query and documents.
        """
        try:
            query_embed = self.embed_text(query, model=model, input_type="search_query")
            if "error" in query_embed:
                raise ValueError(f"Query embedding failed: {query_embed['error']}")

            doc_embeds = self.embed_batch(
                documents, model=model, input_type="search_document"
            )

            query_vector = np.array(query_embed["embedding"])
            similarities = []

            for doc_embed in doc_embeds:
                if "error" in doc_embed:
                    similarity = -1
                else:
                    doc_vector = np.array(doc_embed["embedding"])
                    similarity = np.dot(query_vector, doc_vector) / (
                        np.linalg.norm(query_vector) * np.linalg.norm(doc_vector)
                    )

                similarities.append(
                    {
                        "document": doc_embed["text"],
                        "similarity": float(similarity),
                        "embedding": doc_embed.get("embedding"),
                        "error": doc_embed.get("error"),
                    }
                )

            similarities.sort(key=lambda x: x["similarity"], reverse=True)

            return similarities[:top_k]

        except Exception as e:
            return [{"error": str(e), "query": query, "provider": "cohere"}]

    def get_embedding_models(self) -> List[Dict[str, Any]]:
        """
        Get available embedding models from Cohere.
        """
        models = [
            {
                "name": "embed-english-v3.0",
                "dimensions": 1024,
                "max_tokens": 512,
                "languages": ["en"],
                "description": "English language embeddings",
            },
            {
                "name": "embed-multilingual-v3.0",
                "dimensions": 1024,
                "max_tokens": 512,
                "languages": ["multilingual"],
                "description": "Multilingual embeddings",
            },
            {
                "name": "embed-english-light-v3.0",
                "dimensions": 384,
                "max_tokens": 512,
                "languages": ["en"],
                "description": "Lightweight English embeddings",
            },
            {
                "name": "embed-multilingual-light-v3.0",
                "dimensions": 384,
                "max_tokens": 512,
                "languages": ["multilingual"],
                "description": "Lightweight multilingual embeddings",
            },
        ]

        return models


def embed_platform_output(
    text: str, model: str = "embed-english-v3.0", input_type: str = "search_document"
) -> Dict[str, Any]:
    """
    Embed platform model output for evaluation or retrieval.
    """
    embedder = CohereEmbedder()
    return embedder.embed_text(text, model, input_type)


def embed_model_response(
    model_response: Dict[str, Any], include_metadata: bool = False
) -> Dict[str, Any]:
    """
    Embed a complete model response.
    """
    text = model_response.get("text", "")

    embedding_result = embed_platform_output(text)

    embedded_response = model_response.copy()
    embedded_response["embedding"] = embedding_result.get("embedding")
    embedded_response["embedding_metadata"] = embedding_result

    if include_metadata:
        metadata_text = str(model_response.get("metadata", {}))
        if metadata_text:
            metadata_embedding = embed_platform_output(
                metadata_text, input_type="classification"
            )
            embedded_response["metadata_embedding"] = metadata_embedding.get(
                "embedding"
            )

    return embedded_response


def create_embedding_index(
    texts: List[str], model: str = "embed-english-v3.0"
) -> Dict[str, Any]:
    """
    Create an embedding index for a collection of texts.
    """
    embedder = CohereEmbedder()

    embeddings = embedder.embed_batch(texts, model=model)

    vectors = []
    valid_texts = []
    for embed in embeddings:
        if "embedding" in embed:
            vectors.append(embed["embedding"])
            valid_texts.append(embed["text"])

    if not vectors:
        return {"error": "No valid embeddings generated", "provider": "cohere"}

    vectors_array = np.array(vectors)

    return {
        "texts": valid_texts,
        "embeddings": vectors,
        "embeddings_array": vectors_array,
        "dimension": vectors_array.shape[1],
        "count": vectors_array.shape[0],
        "model": model,
        "provider": "cohere",
    }
