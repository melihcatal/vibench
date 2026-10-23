import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import boto3
from botocore.exceptions import ClientError


@dataclass
class AuditNote:
    """Model for crypto audit notes."""

    operation: str
    key_id: str
    timestamp: str
    user_id: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    payload_size: Optional[int] = None
    algorithm: Optional[str] = None
    additional_notes: Optional[str] = None

    def to_text(self) -> str:
        """Convert audit note to text for embedding."""
        text_parts = [
            f"Operation: {self.operation}",
            f"Key: {self.key_id}",
            f"Time: {self.timestamp}",
            f"Status: {'Success' if self.success else 'Failed'}",
        ]

        if self.user_id:
            text_parts.append(f"User: {self.user_id}")

        if self.algorithm:
            text_parts.append(f"Algorithm: {self.algorithm}")

        if self.payload_size:
            text_parts.append(f"Payload size: {self.payload_size} bytes")

        if self.error_message:
            text_parts.append(f"Error: {self.error_message}")

        if self.additional_notes:
            text_parts.append(f"Notes: {self.additional_notes}")

        return " | ".join(text_parts)


class CryptoAuditEmbedder:
    """Embed crypto audit notes for semantic search using AWS Bedrock."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.bedrock = boto3.client("bedrock-runtime", region_name=self.region)

        # Bedrock model ID for embeddings
        self.embedding_model_id = os.getenv(
            "BEDROCK_EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0"
        )

        # Initialize OpenSearch client if available
        self.opensearch_client = None
        opsearch_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
        if opsearch_endpoint:
            from opensearchpy import OpenSearch

            self.opensearch_client = OpenSearch(
                hosts=[opsearch_endpoint],
                http_auth=(
                    os.getenv("OPENSEARCH_USER"),
                    os.getenv("OPENSEARCH_PASSWORD"),
                ),
                use_ssl=True,
                verify_certs=True,
            )

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using AWS Bedrock.

        Args:
            text: Text to embed

        Returns:
            List of float embedding values
        """
        try:
            # Prepare request for Titan embedding model
            if "titan" in self.embedding_model_id.lower():
                request_body = json.dumps(
                    {
                        "inputText": text,
                        "dimensions": 1024,  # Titan v2 supports configurable dimensions
                    }
                )
            else:
                # Generic request format
                request_body = json.dumps({"inputText": text})

            response = self.bedrock.invoke_model(
                modelId=self.embedding_model_id,
                body=request_body,
                contentType="application/json",
                accept="application/json",
            )

            response_body = json.loads(response["body"].read())

            # Extract embedding based on model response format
            if "embedding" in response_body:
                embedding = response_body["embedding"]
            elif "embeddings" in response_body and response_body["embeddings"]:
                embedding = response_body["embeddings"][0]
            else:
                # Try to find any list of floats in response
                for key, value in response_body.items():
                    if (
                        isinstance(value, list)
                        and len(value) > 0
                        and isinstance(value[0], (int, float))
                    ):
                        embedding = value
                        break
                else:
                    raise ValueError("Could not extract embedding from response")

            return embedding

        except ClientError as e:
            raise Exception(f"AWS Bedrock embedding failed: {e}")

    def embed_audit_note(self, audit_note: AuditNote) -> Dict[str, Any]:
        """
        Create embedding for a single audit note.

        Args:
            audit_note: AuditNote object

        Returns:
            Dictionary with note and embedding
        """
        note_text = audit_note.to_text()

        try:
            embedding = self.generate_embedding(note_text)

            return {
                "note": asdict(audit_note),
                "text": note_text,
                "embedding": embedding,
                "embedding_model": self.embedding_model_id,
                "embedding_dimensions": len(embedding),
                "provider": "aws_bedrock",
            }
        except Exception as e:
            # Fallback to simple keyword extraction if embedding fails
            return {
                "note": asdict(audit_note),
                "text": note_text,
                "embedding": [],
                "error": str(e),
                "provider": "fallback",
            }

    def embed_batch_audit_notes(
        self, audit_notes: List[AuditNote]
    ) -> List[Dict[str, Any]]:
        """
        Create embeddings for multiple audit notes.

        Args:
            audit_notes: List of AuditNote objects

        Returns:
            List of embedded notes
        """
        embedded_notes = []

        for note in audit_notes:
            try:
                embedded_note = self.embed_audit_note(note)
                embedded_notes.append(embedded_note)
            except Exception as e:
                # Log error but continue with other notes
                print(f"Failed to embed note: {e}")
                embedded_notes.append(
                    {
                        "note": asdict(note),
                        "text": note.to_text(),
                        "embedding": [],
                        "error": str(e),
                        "provider": "error",
                    }
                )

        return embedded_notes

    def store_in_opensearch(
        self, embedded_note: Dict[str, Any], index_name: str = "crypto-audit-notes"
    ) -> bool:
        """
        Store embedded audit note in OpenSearch for semantic search.

        Args:
            embedded_note: Embedded note dictionary
            index_name: OpenSearch index name

        Returns:
            True if successful, False otherwise
        """
        if not self.opensearch_client:
            return False

        try:
            # Create index if it doesn't exist
            if not self.opensearch_client.indices.exists(index=index_name):
                index_body = {
                    "settings": {
                        "index": {"knn": True, "knn.algo_param.ef_search": 100}
                    },
                    "mappings": {
                        "properties": {
                            "note": {"type": "object", "enabled": True},
                            "text": {"type": "text"},
                            "embedding": {
                                "type": "knn_vector",
                                "dimension": embedded_note.get(
                                    "embedding_dimensions", 1024
                                ),
                            },
                            "embedding_model": {"type": "keyword"},
                            "provider": {"type": "keyword"},
                            "timestamp": {"type": "date"},
                        }
                    },
                }
                self.opensearch_client.indices.create(index=index_name, body=index_body)

            # Prepare document
            document = {
                "note": embedded_note["note"],
                "text": embedded_note["text"],
                "embedding": embedded_note.get("embedding", []),
                "embedding_model": embedded_note.get("embedding_model", ""),
                "provider": embedded_note.get("provider", ""),
                "timestamp": embedded_note["note"].get("timestamp", ""),
            }

            # Index document
            response = self.opensearch_client.index(
                index=index_name, body=document, refresh=True
            )

            return response["result"] == "created"

        except Exception as e:
            print(f"Failed to store in OpenSearch: {e}")
            return False

    def search_similar_notes(
        self, query_text: str, index_name: str = "crypto-audit-notes", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for similar audit notes using semantic search.

        Args:
            query_text: Search query text
            index_name: OpenSearch index name
            limit: Maximum number of results

        Returns:
            List of similar notes with scores
        """
        if not self.opensearch_client:
            return []

        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query_text)

            # Search using k-NN
            search_body = {
                "size": limit,
                "query": {
                    "knn": {"embedding": {"vector": query_embedding, "k": limit}}
                },
                "_source": ["note", "text", "embedding_model", "provider"],
            }

            response = self.opensearch_client.search(index=index_name, body=search_body)

            results = []
            for hit in response["hits"]["hits"]:
                results.append(
                    {
                        "score": hit["_score"],
                        "note": hit["_source"]["note"],
                        "text": hit["_source"]["text"],
                        "provider": hit["_source"].get("provider", ""),
                    }
                )

            return results

        except Exception as e:
            print(f"Search failed: {e}")
            return []

    def generate_audit_summary(self, audit_notes: List[AuditNote]) -> Dict[str, Any]:
        """
        Generate semantic summary of audit notes using AWS Bedrock.

        Args:
            audit_notes: List of audit notes

        Returns:
            Semantic summary
        """
        if not audit_notes:
            return {"summary": "No audit notes available", "provider": "aws_bedrock"}

        # Combine note texts
        combined_text = "\n".join(
            [note.to_text() for note in audit_notes[:50]]
        )  # Limit to 50 notes

        try:
            # Use Bedrock for summarization
            summary_model_id = os.getenv(
                "BEDROCK_SUMMARY_MODEL", "amazon.titan-text-express-v1"
            )

            prompt = f"""
            Analyze these cryptographic audit notes and provide a summary:
            
            {combined_text}
            
            Provide a concise summary covering:
            1. Overall success/failure rates
            2. Most common operations
            3. Key usage patterns
            4. Any concerning patterns or errors
            5. Recommendations for improvement
            
            Summary:
            """

            request_body = json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 500,
                        "temperature": 0.2,
                        "topP": 0.9,
                    },
                }
            )

            response = self.bedrock.invoke_model(
                modelId=summary_model_id,
                body=request_body,
                contentType="application/json",
                accept="application/json",
            )

            response_body = json.loads(response["body"].read())

            if "results" in response_body and response_body["results"]:
                summary_text = response_body["results"][0]["outputText"]
            elif "generation" in response_body:
                summary_text = response_body["generation"]
            else:
                summary_text = str(response_body)

            return {
                "summary": summary_text.strip(),
                "notes_analyzed": len(audit_notes),
                "summary_model": summary_model_id,
                "provider": "aws_bedrock",
            }

        except Exception as e:
            # Fallback to simple statistical summary
            success_count = sum(1 for note in audit_notes if note.success)
            operations = {}
            for note in audit_notes:
                operations[note.operation] = operations.get(note.operation, 0) + 1

            return {
                "summary": f"Analyzed {len(audit_notes)} notes. Success rate: {success_count / len(audit_notes) * 100:.1f}%. Operations: {operations}",
                "notes_analyzed": len(audit_notes),
                "success_rate": success_count / len(audit_notes),
                "operations": operations,
                "provider": "fallback",
                "error": str(e),
            }


if __name__ == "__main__":
    embedder = CryptoAuditEmbedder()

    # Create sample audit notes
    notes = [
        AuditNote(
            operation="encrypt",
            key_id="alias/encryption-key",
            timestamp="2024-01-15T10:30:00Z",
            user_id="user123",
            success=True,
            payload_size=1024,
            algorithm="AES-256-GCM",
        ),
        AuditNote(
            operation="decrypt",
            key_id="alias/encryption-key",
            timestamp="2024-01-15T11:15:00Z",
            user_id="user456",
            success=False,
            error_message="Invalid ciphertext format",
            algorithm="AES-256-GCM",
        ),
        AuditNote(
            operation="sign",
            key_id="alias/signing-key",
            timestamp="2024-01-15T12:00:00Z",
            user_id="user789",
            success=True,
            payload_size=512,
            algorithm="RSASSA_PSS_SHA_256",
            additional_notes="Document signing for contract",
        ),
    ]

    # Embed a single note
    embedded_note = embedder.embed_audit_note(notes[0])
    print(f"Embedded note: {json.dumps(embedded_note, indent=2)}")

    # Generate summary
    summary = embedder.generate_audit_summary(notes)
    print(f"\nAudit summary: {json.dumps(summary, indent=2)}")
