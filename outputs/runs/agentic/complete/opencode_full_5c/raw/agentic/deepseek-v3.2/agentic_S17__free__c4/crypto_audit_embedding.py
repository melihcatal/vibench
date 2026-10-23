import os
import json
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
from google.cloud import aiplatform
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchableField,
)


class CryptoAuditEmbedding:
    """Embed crypto audit notes for semantic search using various providers."""

    def __init__(self):
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID", "my-project")
        self.gcp_location = os.environ.get("GCP_LOCATION", "us-central1")
        self.azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
        self.azure_search_key = os.environ.get("AZURE_SEARCH_KEY", "")

    def generate_embedding(
        self, text: str, provider: str = "openai", **kwargs
    ) -> List[float]:
        """
        Generate embedding vector for text.

        Args:
            text: Text to embed
            provider: 'openai', 'aws', 'gcp', or 'azure'
            **kwargs: Provider-specific arguments

        Returns:
            Embedding vector as list of floats
        """
        if not text:
            return []

        if provider.lower() == "openai":
            return self._embed_with_openai(text, **kwargs)
        elif provider.lower() == "aws":
            return self._embed_with_aws_bedrock(text, **kwargs)
        elif provider.lower() == "gcp":
            return self._embed_with_gcp_vertex(text, **kwargs)
        elif provider.lower() == "azure":
            return self._embed_with_azure_openai(text, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _embed_with_openai(self, text: str, **kwargs) -> List[float]:
        """Generate embedding using OpenAI."""
        if not self.openai_api_key:
            # Fallback to a simple hash-based embedding
            return self._simple_hash_embedding(text)

        try:
            client = OpenAI(api_key=self.openai_api_key)

            model = kwargs.get("model", "text-embedding-3-small")

            response = client.embeddings.create(
                model=model, input=text, encoding_format="float"
            )

            return response.data[0].embedding

        except Exception as e:
            print(f"OpenAI embedding error: {e}")
            return self._simple_hash_embedding(text)

    def _embed_with_aws_bedrock(self, text: str, **kwargs) -> List[float]:
        """Generate embedding using AWS Bedrock."""
        bedrock_client = boto3.client("bedrock-runtime", region_name=self.aws_region)

        try:
            model_id = kwargs.get("model_id", "amazon.titan-embed-text-v1")

            if model_id.startswith("amazon.titan"):
                # Titan embedding model
                body = json.dumps({"inputText": text})

                response = bedrock_client.invoke_model(
                    modelId=model_id,
                    body=body,
                    accept="application/json",
                    contentType="application/json",
                )

                response_body = json.loads(response["body"].read())
                embedding = response_body.get("embedding", [])

                return embedding

            elif model_id.startswith("cohere"):
                # Cohere embedding model
                body = json.dumps({"texts": [text], "input_type": "search_document"})

                response = bedrock_client.invoke_model(
                    modelId=model_id,
                    body=body,
                    accept="application/json",
                    contentType="application/json",
                )

                response_body = json.loads(response["body"].read())
                embeddings = response_body.get("embeddings", [[]])

                return embeddings[0] if embeddings else []

            else:
                raise ValueError(f"Unsupported AWS Bedrock model: {model_id}")

        except ClientError as e:
            print(f"AWS Bedrock embedding error: {e}")
            return self._simple_hash_embedding(text)

    def _embed_with_gcp_vertex(self, text: str, **kwargs) -> List[float]:
        """Generate embedding using Google Cloud Vertex AI."""
        try:
            # Initialize Vertex AI
            aiplatform.init(project=self.gcp_project_id, location=self.gcp_location)

            from google.cloud import aiplatform_v1

            # Use text embedding model
            model = kwargs.get("model", "textembedding-gecko@001")

            # Create prediction client
            endpoint = aiplatform.Endpoint(
                f"projects/{self.gcp_project_id}/locations/{self.gcp_location}/publishers/google/models/{model}"
            )

            # Make prediction
            predictions = endpoint.predict(instances=[{"content": text}])

            if predictions and predictions.predictions:
                embedding = (
                    predictions.predictions[0].get("embeddings", {}).get("values", [])
                )
                return embedding

            return []

        except Exception as e:
            print(f"GCP Vertex AI embedding error: {e}")
            return self._simple_hash_embedding(text)

    def _embed_with_azure_openai(self, text: str, **kwargs) -> List[float]:
        """Generate embedding using Azure OpenAI."""
        azure_openai_key = os.environ.get("AZURE_OPENAI_KEY", "")
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")

        if not azure_openai_key or not azure_openai_endpoint:
            return self._simple_hash_embedding(text)

        try:
            from openai import AzureOpenAI

            client = AzureOpenAI(
                api_key=azure_openai_key,
                api_version="2023-12-01-preview",
                azure_endpoint=azure_openai_endpoint,
            )

            deployment = kwargs.get("deployment", "text-embedding-ada-002")

            response = client.embeddings.create(model=deployment, input=text)

            return response.data[0].embedding

        except Exception as e:
            print(f"Azure OpenAI embedding error: {e}")
            return self._simple_hash_embedding(text)

    def _simple_hash_embedding(self, text: str, dimension: int = 128) -> List[float]:
        """Generate a simple deterministic embedding for fallback."""
        import hashlib

        # Create a deterministic hash-based embedding
        hash_obj = hashlib.sha256(text.encode("utf-8"))
        hash_bytes = hash_obj.digest()

        # Convert to list of floats
        embedding = []
        for i in range(dimension):
            if i < len(hash_bytes):
                # Normalize byte to [-1, 1]
                val = (hash_bytes[i] / 127.5) - 1.0
            else:
                # Use pseudo-random based on position
                val = np.sin(i * 0.1) * 0.5

            embedding.append(float(val))

        return embedding

    def create_audit_note_embedding(
        self, audit_note: Dict, provider: str = "openai"
    ) -> Dict:
        """
        Create embedding for a crypto audit note.

        Args:
            audit_note: Audit note dictionary
            provider: Embedding provider

        Returns:
            Dict with note and embedding
        """
        # Extract text for embedding
        text_parts = []

        if "operation" in audit_note:
            text_parts.append(f"Operation: {audit_note['operation']}")

        if "key_id" in audit_note:
            text_parts.append(f"Key: {audit_note['key_id']}")

        if "description" in audit_note:
            text_parts.append(f"Description: {audit_note['description']}")

        if "findings" in audit_note:
            if isinstance(audit_note["findings"], str):
                text_parts.append(f"Findings: {audit_note['findings']}")
            elif isinstance(audit_note["findings"], list):
                text_parts.append(f"Findings: {', '.join(audit_note['findings'])}")

        if "recommendations" in audit_note:
            if isinstance(audit_note["recommendations"], str):
                text_parts.append(f"Recommendations: {audit_note['recommendations']}")
            elif isinstance(audit_note["recommendations"], list):
                text_parts.append(
                    f"Recommendations: {', '.join(audit_note['recommendations'])}"
                )

        text = " ".join(text_parts)

        # Generate embedding
        embedding = self.generate_embedding(text, provider)

        # Create result
        result = {
            "id": audit_note.get("id", f"audit_{datetime.utcnow().timestamp()}"),
            "timestamp": audit_note.get(
                "timestamp", datetime.utcnow().isoformat() + "Z"
            ),
            "operation": audit_note.get("operation", ""),
            "key_id": audit_note.get("key_id", ""),
            "provider": audit_note.get("provider", ""),
            "description": audit_note.get("description", ""),
            "findings": audit_note.get("findings", []),
            "recommendations": audit_note.get("recommendations", []),
            "embedding": embedding,
            "embedding_provider": provider,
            "embedding_dimension": len(embedding),
            "text_for_embedding": text,
        }

        return result

    def search_similar_audit_notes(
        self, query: str, notes: List[Dict], provider: str = "openai", top_k: int = 5
    ) -> List[Dict]:
        """
        Search for similar audit notes using semantic search.

        Args:
            query: Search query
            notes: List of audit notes with embeddings
            provider: Embedding provider for query
            top_k: Number of results to return

        Returns:
            List of similar notes with similarity scores
        """
        if not notes:
            return []

        # Generate embedding for query
        query_embedding = self.generate_embedding(query, provider)

        if not query_embedding:
            return []

        # Calculate similarities
        similarities = []
        for note in notes:
            if "embedding" not in note or not note["embedding"]:
                continue

            note_embedding = note["embedding"]

            # Ensure embeddings have same dimension
            if len(query_embedding) != len(note_embedding):
                continue

            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, note_embedding)

            similarities.append({"note": note, "similarity": similarity})

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top-k results
        return similarities[:top_k]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = np.sqrt(sum(a * a for a in vec1))
        norm2 = np.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def create_azure_search_index(self, index_name: str = "crypto-audit-notes") -> bool:
        """
        Create Azure Cognitive Search index for audit notes.

        Args:
            index_name: Name of the index

        Returns:
            True if successful
        """
        if not self.azure_search_endpoint or not self.azure_search_key:
            return False

        try:
            credential = AzureKeyCredential(self.azure_search_key)
            index_client = SearchIndexClient(
                endpoint=self.azure_search_endpoint, credential=credential
            )

            # Define fields
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SimpleField(
                    name="timestamp",
                    type=SearchFieldDataType.DateTimeOffset,
                    filterable=True,
                    sortable=True,
                ),
                SearchableField(
                    name="operation", type=SearchFieldDataType.String, filterable=True
                ),
                SearchableField(
                    name="key_id", type=SearchFieldDataType.String, filterable=True
                ),
                SearchableField(
                    name="provider", type=SearchFieldDataType.String, filterable=True
                ),
                SearchableField(name="description", type=SearchFieldDataType.String),
                SearchableField(
                    name="findings",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                ),
                SearchableField(
                    name="recommendations",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                ),
                SimpleField(
                    name="embedding",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Double),
                    vector_search_dimensions=1536,
                    vector_search_profile_name="my-vector-profile",
                ),
            ]

            # Configure vector search
            vector_search = VectorSearch(
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="my-hnsw",
                        parameters={
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                            "metric": "cosine",
                        },
                    )
                ],
                profiles=[
                    VectorSearchProfile(
                        name="my-vector-profile", algorithm_configuration_name="my-hnsw"
                    )
                ],
            )

            # Create index
            index = SearchIndex(
                name=index_name, fields=fields, vector_search=vector_search
            )

            index_client.create_index(index)
            return True

        except Exception as e:
            print(f"Azure Search index creation error: {e}")
            return False

    def index_audit_note_in_azure(
        self, note: Dict, index_name: str = "crypto-audit-notes"
    ) -> bool:
        """
        Index an audit note in Azure Cognitive Search.

        Args:
            note: Audit note with embedding
            index_name: Name of the index

        Returns:
            True if successful
        """
        if not self.azure_search_endpoint or not self.azure_search_key:
            return False

        try:
            credential = AzureKeyCredential(self.azure_search_key)
            search_client = SearchClient(
                endpoint=self.azure_search_endpoint,
                index_name=index_name,
                credential=credential,
            )

            # Prepare document
            document = {
                "id": note.get("id", ""),
                "timestamp": note.get("timestamp", ""),
                "operation": note.get("operation", ""),
                "key_id": note.get("key_id", ""),
                "provider": note.get("provider", ""),
                "description": note.get("description", ""),
                "findings": note.get("findings", []),
                "recommendations": note.get("recommendations", []),
                "embedding": note.get("embedding", []),
            }

            # Upload document
            search_client.upload_documents(documents=[document])
            return True

        except Exception as e:
            print(f"Azure Search indexing error: {e}")
            return False
