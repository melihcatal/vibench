import os
import json
from typing import List, Dict, Any
from openai import OpenAI


class SecretAuditEmbeddingGenerator:
    """Generate embeddings for secret audit notes using OpenAI API."""

    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        """
        Initialize embedding generator with OpenAI API.

        Args:
            api_key: OpenAI API key (defaults to environment variable)
            model: Embedding model to use
        """
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        try:
            response = self.client.embeddings.create(
                model=self.model, input=text, encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding: {e}")

    def embed_audit_note(
        self,
        secret_name: str,
        note: str,
        auditor: str,
        risk_level: str = "low",
        labels: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Embed a single audit note with metadata.

        Args:
            secret_name: Name of the secret
            note: Audit note text
            auditor: Name of auditor
            risk_level: Risk level (low, medium, high, critical)
            labels: List of labels/tags

        Returns:
            Dictionary with embedding and metadata
        """
        if labels is None:
            labels = []

        # Prepare text for embedding
        embedding_text = f"""
        Secret: {secret_name}
        Audit Note: {note}
        Auditor: {auditor}
        Risk Level: {risk_level}
        Labels: {", ".join(labels)}
        """

        # Generate embedding
        embedding = self.generate_embedding(embedding_text)

        # Create metadata
        metadata = {
            "secret_name": secret_name,
            "note": note,
            "auditor": auditor,
            "risk_level": risk_level,
            "labels": labels,
            "embedding_model": self.model,
            "embedding_dimensions": len(embedding),
        }

        return {
            "embedding": embedding,
            "metadata": metadata,
            "text": embedding_text.strip(),
        }

    def embed_batch_audit_notes(
        self, audit_notes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Embed multiple audit notes in batch.

        Args:
            audit_notes: List of audit note dictionaries

        Returns:
            List of embedded audit notes
        """
        # Prepare texts for batch embedding
        texts = []
        metadata_list = []

        for note_data in audit_notes:
            secret_name = note_data.get("secret_name", "")
            note = note_data.get("note", "")
            auditor = note_data.get("auditor", "")
            risk_level = note_data.get("risk_level", "low")
            labels = note_data.get("labels", [])

            embedding_text = f"""
            Secret: {secret_name}
            Audit Note: {note}
            Auditor: {auditor}
            Risk Level: {risk_level}
            Labels: {", ".join(labels)}
            """

            texts.append(embedding_text.strip())

            metadata = {
                "secret_name": secret_name,
                "note": note,
                "auditor": auditor,
                "risk_level": risk_level,
                "labels": labels,
            }
            metadata_list.append(metadata)

        try:
            # Batch embedding request
            response = self.client.embeddings.create(
                model=self.model, input=texts, encoding_format="float"
            )

            # Combine embeddings with metadata
            results = []
            for i, embedding_data in enumerate(response.data):
                result = {
                    "embedding": embedding_data.embedding,
                    "metadata": metadata_list[i],
                    "text": texts[i],
                    "embedding_model": self.model,
                    "embedding_dimensions": len(embedding_data.embedding),
                }
                results.append(result)

            return results

        except Exception as e:
            raise RuntimeError(f"Failed to generate batch embeddings: {e}")

    def search_similar_notes(
        self, query: str, embedded_notes: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar audit notes using cosine similarity.

        Args:
            query: Search query text
            embedded_notes: List of embedded audit notes
            top_k: Number of top results to return

        Returns:
            List of similar notes with similarity scores
        """
        # Generate embedding for query
        query_embedding = self.generate_embedding(query)

        # Calculate cosine similarities
        similarities = []
        for note in embedded_notes:
            note_embedding = note["embedding"]

            # Cosine similarity
            dot_product = sum(q * n for q, n in zip(query_embedding, note_embedding))
            query_norm = sum(q * q for q in query_embedding) ** 0.5
            note_norm = sum(n * n for n in note_embedding) ** 0.5

            if query_norm == 0 or note_norm == 0:
                similarity = 0
            else:
                similarity = dot_product / (query_norm * note_norm)

            similarities.append(
                {
                    "similarity": similarity,
                    "metadata": note["metadata"],
                    "text": note["text"],
                }
            )

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top_k results
        return similarities[:top_k]

    def save_embeddings_to_file(
        self, embedded_notes: List[Dict[str, Any]], filepath: str
    ) -> None:
        """
        Save embeddings to a JSON file.

        Args:
            embedded_notes: List of embedded audit notes
            filepath: Path to save file
        """
        # Convert embeddings to serializable format
        serializable_notes = []
        for note in embedded_notes:
            serializable_note = {
                "embedding": note["embedding"],
                "metadata": note["metadata"],
                "text": note["text"],
                "embedding_model": note.get("embedding_model", self.model),
                "embedding_dimensions": note.get(
                    "embedding_dimensions", len(note["embedding"])
                ),
            }
            serializable_notes.append(serializable_note)

        try:
            with open(filepath, "w") as f:
                json.dump(serializable_notes, f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save embeddings to file: {e}")

    def load_embeddings_from_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load embeddings from a JSON file.

        Args:
            filepath: Path to load file from

        Returns:
            List of embedded audit notes
        """
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Ensure embeddings are lists of floats
            for note in data:
                if "embedding" in note and isinstance(note["embedding"], list):
                    note["embedding"] = [float(x) for x in note["embedding"]]

            return data
        except Exception as e:
            raise RuntimeError(f"Failed to load embeddings from file: {e}")
