import os
from typing import List, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform import matching_engine
from google.cloud.aiplatform.matching_engine import MatchingEngineIndexEndpoint
import vertexai
from vertexai.language_models import TextEmbeddingModel


class CryptoAuditEmbedder:
    """Embed crypto audit notes for semantic search using Google Vertex AI."""

    def __init__(self, project_id: str = None, location: str = "us-central1"):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location

        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)

        # Initialize embedding model
        self.embedding_model = TextEmbeddingModel.from_pretrained(
            "textembedding-gecko@003"
        )

        # Initialize Matching Engine client (for production use)
        self.index_endpoint = None
        self.index_id = os.environ.get("VERTEX_AI_INDEX_ID")
        self.endpoint_id = os.environ.get("VERTEX_AI_ENDPOINT_ID")

    def embed_audit_note(
        self, audit_note: str, metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Embed a single crypto audit note."""

        # Generate embedding
        embeddings = self.embedding_model.get_embeddings([audit_note])
        embedding_vector = embeddings[0].values

        # Prepare metadata
        if metadata is None:
            metadata = {}

        metadata.update(
            {
                "provider": "google-vertex-ai",
                "embedding_model": "textembedding-gecko@003",
                "embedding_dimensions": len(embedding_vector),
            }
        )

        return {
            "id": f"audit_{hash(audit_note)}",
            "text": audit_note,
            "embedding": embedding_vector,
            "metadata": metadata,
            "embedding_info": {
                "model": "textembedding-gecko@003",
                "dimensions": len(embedding_vector),
                "provider": "google-vertex-ai",
            },
        }

    def embed_batch_audit_notes(
        self, audit_notes: List[str], metadatas: List[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Embed multiple crypto audit notes in batch."""

        if metadatas is None:
            metadatas = [{}] * len(audit_notes)

        # Generate embeddings in batch
        embeddings = self.embedding_model.get_embeddings(audit_notes)

        results = []
        for i, (note, metadata, embedding) in enumerate(
            zip(audit_notes, metadatas, embeddings)
        ):
            metadata.update(
                {
                    "provider": "google-vertex-ai",
                    "embedding_model": "textembedding-gecko@003",
                    "embedding_dimensions": len(embedding.values),
                }
            )

            results.append(
                {
                    "id": f"audit_batch_{i}_{hash(note)}",
                    "text": note,
                    "embedding": embedding.values,
                    "metadata": metadata,
                    "embedding_info": {
                        "model": "textembedding-gecko@003",
                        "dimensions": len(embedding.values),
                        "provider": "google-vertex-ai",
                    },
                }
            )

        return results

    def search_similar_audits(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar audit notes using semantic search."""

        # Generate query embedding
        query_embedding = self.embedding_model.get_embeddings([query])[0].values

        # For demo purposes, we'll return a mock response
        # In production, you would query a Matching Engine index

        mock_similar_audits = [
            {
                "id": "audit_123",
                "text": "Encryption key rotation completed for production database",
                "similarity_score": 0.92,
                "metadata": {
                    "timestamp": "2024-01-15T10:30:00Z",
                    "key_name": "projects/my-project/locations/global/keyRings/prod-ring/cryptoKeys/db-encryption-key",
                    "operation": "key_rotation",
                },
            },
            {
                "id": "audit_456",
                "text": "Security audit of KMS key usage patterns",
                "similarity_score": 0.85,
                "metadata": {
                    "timestamp": "2024-01-10T14:20:00Z",
                    "key_name": "projects/my-project/locations/global/keyRings/prod-ring/cryptoKeys/api-signing-key",
                    "operation": "security_audit",
                },
            },
            {
                "id": "audit_789",
                "text": "Compliance check for encryption standards",
                "similarity_score": 0.78,
                "metadata": {
                    "timestamp": "2024-01-05T09:15:00Z",
                    "key_name": "projects/my-project/locations/global/keyRings/prod-ring/cryptoKeys/compliance-key",
                    "operation": "compliance_check",
                },
            },
        ]

        return {
            "query": query,
            "query_embedding_dimensions": len(query_embedding),
            "top_k": top_k,
            "provider": "google-vertex-ai",
            "similar_audits": mock_similar_audits,
            "embedding_model": "textembedding-gecko@003",
        }

    def create_audit_index(
        self,
        audit_embeddings: List[Dict[str, Any]],
        index_name: str = "crypto-audit-index",
    ) -> Dict[str, Any]:
        """Create a search index for audit embeddings (mock implementation)."""

        # In production, this would create a Matching Engine index
        # For demo, return mock index info

        return {
            "index_name": index_name,
            "provider": "google-vertex-ai",
            "index_type": "matching_engine",
            "embeddings_count": len(audit_embeddings),
            "dimensions": len(audit_embeddings[0]["embedding"])
            if audit_embeddings
            else 0,
            "status": "MOCK_INDEX_CREATED",
            "model": "textembedding-gecko@003",
            "note": "In production, this would create a Vertex AI Matching Engine index",
        }


def embed_crypto_audit_notes(audit_notes: List[str]) -> List[Dict[str, Any]]:
    """Embed crypto audit notes for semantic search."""
    embedder = CryptoAuditEmbedder()
    return embedder.embed_batch_audit_notes(audit_notes)


if __name__ == "__main__":
    # Example usage
    audit_notes = [
        "Key rotation completed for database encryption key on 2024-01-15",
        "Security audit found proper key usage patterns in production",
        "Compliance check passed for encryption standards PCI-DSS and HIPAA",
    ]

    embeddings = embed_crypto_audit_notes(audit_notes)
    print(f"Embedded {len(embeddings)} audit notes")

    # Search example
    embedder = CryptoAuditEmbedder()
    search_results = embedder.search_similar_audits("key rotation audit", top_k=3)
    print(f"Search results: {search_results}")
