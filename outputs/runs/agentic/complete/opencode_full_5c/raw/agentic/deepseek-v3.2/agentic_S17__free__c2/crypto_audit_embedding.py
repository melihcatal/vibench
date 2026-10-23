import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
import pinecone


def embed_crypto_audit_notes(
    audit_data: Dict[str, Any], embedding_provider: str = "openai"
) -> Dict[str, Any]:
    """
    Embed crypto audit notes for semantic search using AI embeddings.

    Args:
        audit_data: Crypto audit data from key_usage_summary.py
        embedding_provider: Provider for embeddings ('openai', 'aws', or 'cohere')

    Returns:
        Dictionary with embeddings and metadata
    """
    if embedding_provider == "openai":
        return _embed_with_openai(audit_data)
    elif embedding_provider == "aws":
        return _embed_with_aws(audit_data)
    elif embedding_provider == "cohere":
        return _embed_with_cohere(audit_data)
    else:
        raise ValueError(f"Unsupported embedding provider: {embedding_provider}")


def _embed_with_openai(audit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate embeddings using OpenAI API."""
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Prepare text for embedding
        embed_text = _prepare_embedding_text(audit_data)

        # Generate embedding
        response = client.embeddings.create(
            model="text-embedding-3-small", input=embed_text, encoding_format="float"
        )

        embedding = response.data[0].embedding

        # Store in Pinecone vector database
        pinecone_result = _store_in_pinecone(
            vector=embedding, metadata=audit_data, namespace="crypto_audits"
        )

        # Prepare embedding result
        embedding_result = {
            "embedding": embedding[:10],  # First 10 dimensions for reference
            "embedding_dimensions": len(embedding),
            "embedding_model": "text-embedding-3-small",
            "text_length": len(embed_text),
            "pinecone_storage": pinecone_result,
            "provider": "openai",
            "generated_at": datetime.utcnow().isoformat(),
        }

        return embedding_result

    except Exception as e:
        raise Exception(f"OpenAI embedding failed: {str(e)}")


def _embed_with_aws(audit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate embeddings using AWS Bedrock."""
    try:
        # Initialize AWS Bedrock client
        bedrock_client = boto3.client(
            "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

        # Prepare text for embedding
        embed_text = _prepare_embedding_text(audit_data)

        # Call Titan Embeddings model
        model_id = "amazon.titan-embed-text-v1"

        body = json.dumps({"inputText": embed_text})

        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])

        # Store in Pinecone vector database
        pinecone_result = _store_in_pinecone(
            vector=embedding, metadata=audit_data, namespace="crypto_audits_aws"
        )

        # Prepare embedding result
        embedding_result = {
            "embedding": embedding[:10],  # First 10 dimensions for reference
            "embedding_dimensions": len(embedding),
            "embedding_model": model_id,
            "text_length": len(embed_text),
            "pinecone_storage": pinecone_result,
            "provider": "aws_bedrock",
            "generated_at": datetime.utcnow().isoformat(),
        }

        return embedding_result

    except ClientError as e:
        raise Exception(f"AWS Bedrock embedding failed: {str(e)}")


def _embed_with_cohere(audit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate embeddings using Cohere API."""
    try:
        import cohere

        # Initialize Cohere client
        co = cohere.Client(os.environ.get("COHERE_API_KEY"))

        # Prepare text for embedding
        embed_text = _prepare_embedding_text(audit_data)

        # Generate embedding
        response = co.embed(
            texts=[embed_text], model="embed-english-v3.0", input_type="search_document"
        )

        embedding = response.embeddings[0]

        # Store in Pinecone vector database
        pinecone_result = _store_in_pinecone(
            vector=embedding, metadata=audit_data, namespace="crypto_audits_cohere"
        )

        # Prepare embedding result
        embedding_result = {
            "embedding": embedding[:10],  # First 10 dimensions for reference
            "embedding_dimensions": len(embedding),
            "embedding_model": "embed-english-v3.0",
            "text_length": len(embed_text),
            "pinecone_storage": pinecone_result,
            "provider": "cohere",
            "generated_at": datetime.utcnow().isoformat(),
        }

        return embedding_result

    except ImportError:
        raise Exception("Cohere client not installed. Install with: pip install cohere")
    except Exception as e:
        raise Exception(f"Cohere embedding failed: {str(e)}")


def _prepare_embedding_text(audit_data: Dict[str, Any]) -> str:
    """Prepare text from audit data for embedding."""
    text_parts = []

    # Key metadata
    if "key_metadata" in audit_data:
        metadata = audit_data["key_metadata"]
        text_parts.append(f"Key ID: {metadata.get('id', '')}")
        text_parts.append(f"Key State: {metadata.get('state', '')}")
        text_parts.append(f"Key Usage: {metadata.get('usage', '')}")
        text_parts.append(f"Created: {metadata.get('created', '')}")
        text_parts.append(f"Enabled: {metadata.get('enabled', '')}")

    # Usage analysis
    if "usage_analysis" in audit_data:
        usage = audit_data["usage_analysis"]
        text_parts.append(f"Total Operations: {usage.get('total_operations', 0)}")
        text_parts.append(
            f"Average Daily Operations: {usage.get('average_daily_operations', 0)}"
        )
        text_parts.append(
            f"Peak Daily Operations: {usage.get('peak_daily_operations', 0)}"
        )

    # Event analysis
    if "event_analysis" in audit_data:
        events = audit_data["event_analysis"]
        text_parts.append(f"Total Events: {events.get('total_events', 0)}")

        # Add event breakdown
        if "event_breakdown" in events:
            for event_name, count in events["event_breakdown"].items():
                text_parts.append(f"{event_name}: {count}")

    # Security configuration
    if "security_configuration" in audit_data:
        config = audit_data["security_configuration"]
        text_parts.append(
            f"Key Rotation Enabled: {config.get('key_rotation_enabled', False)}"
        )
        text_parts.append(
            f"Automatic Rotation: {config.get('automatic_rotation', False)}"
        )
        text_parts.append(
            f"Policy Statements: {config.get('policy_statement_count', 0)}"
        )
        text_parts.append(f"Active Grants: {config.get('active_grants', 0)}")

    # Compliance checks
    if "compliance_checks" in audit_data:
        compliance = audit_data["compliance_checks"]

        for standard, checks in compliance.items():
            text_parts.append(f"{standard} Compliance:")
            for check_name, check_result in checks.items():
                text_parts.append(f"  {check_name}: {check_result}")

    # Recommendations
    if "recommendations" in audit_data:
        recommendations = audit_data["recommendations"]
        if recommendations:
            text_parts.append("Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                text_parts.append(f"  {i}. {rec}")

    return " ".join(text_parts)


def _store_in_pinecone(
    vector: List[float], metadata: Dict[str, Any], namespace: str
) -> Dict[str, Any]:
    """Store embedding in Pinecone vector database."""
    try:
        # Initialize Pinecone
        pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        pinecone_env = os.environ.get("PINECONE_ENVIRONMENT", "us-east-1")

        if not pinecone_api_key:
            return {"stored": False, "reason": "Pinecone API key not configured"}

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

        # Get or create index
        index_name = "crypto-audit-embeddings"

        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=len(vector),
                metric="cosine",
                spec=pinecone.ServerlessSpec(cloud="aws", region=pinecone_env),
            )

        # Connect to index
        index = pinecone.Index(index_name)

        # Generate unique ID
        import hashlib

        metadata_str = json.dumps(metadata, sort_keys=True)
        vector_id = hashlib.md5(metadata_str.encode()).hexdigest()

        # Prepare metadata for storage
        storage_metadata = {
            "key_id": metadata.get("key_metadata", {}).get("id", ""),
            "provider": metadata.get("provider", ""),
            "audit_timestamp": metadata.get("audit_timestamp", ""),
            "risk_level": metadata.get("compliance_checks", {})
            .get("nist_800_57", {})
            .get("key_strength_adequate", ""),
            "recommendations_count": len(metadata.get("recommendations", [])),
        }

        # Upsert vector
        index.upsert(
            vectors=[(vector_id, vector, storage_metadata)], namespace=namespace
        )

        return {
            "stored": True,
            "vector_id": vector_id,
            "index": index_name,
            "namespace": namespace,
            "metadata": storage_metadata,
        }

    except Exception as e:
        return {"stored": False, "error": str(e)}


def search_similar_audits(
    query: str, top_k: int = 5, embedding_provider: str = "openai"
) -> Dict[str, Any]:
    """
    Search for similar crypto audits using semantic search.

    Args:
        query: Search query text
        top_k: Number of results to return
        embedding_provider: Provider for query embedding

    Returns:
        Dictionary with search results
    """
    try:
        # Generate query embedding
        if embedding_provider == "openai":
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = client.embeddings.create(
                model="text-embedding-3-small", input=query, encoding_format="float"
            )
            query_embedding = response.data[0].embedding
        elif embedding_provider == "aws":
            bedrock_client = boto3.client(
                "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
            )
            body = json.dumps({"inputText": query})
            response = bedrock_client.invoke_model(
                body=body,
                modelId="amazon.titan-embed-text-v1",
                accept="application/json",
                contentType="application/json",
            )
            response_body = json.loads(response.get("body").read())
            query_embedding = response_body.get("embedding", [])
        else:
            raise ValueError(f"Unsupported provider for search: {embedding_provider}")

        # Search in Pinecone
        pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        pinecone_env = os.environ.get("PINECONE_ENVIRONMENT", "us-east-1")

        if not pinecone_api_key:
            return {"results": [], "error": "Pinecone API key not configured"}

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

        index_name = "crypto-audit-embeddings"
        if index_name not in pinecone.list_indexes():
            return {"results": [], "error": "Index not found"}

        index = pinecone.Index(index_name)

        # Search in all namespaces
        namespaces = ["crypto_audits", "crypto_audits_aws", "crypto_audits_cohere"]
        all_results = []

        for namespace in namespaces:
            try:
                results = index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True,
                    namespace=namespace,
                )

                for match in results.get("matches", []):
                    all_results.append(
                        {
                            "score": match["score"],
                            "metadata": match["metadata"],
                            "namespace": namespace,
                            "id": match["id"],
                        }
                    )
            except Exception:
                continue

        # Sort by score and limit
        all_results.sort(key=lambda x: x["score"], reverse=True)
        top_results = all_results[:top_k]

        return {
            "query": query,
            "results": top_results,
            "total_matches": len(all_results),
            "embedding_provider": embedding_provider,
            "search_timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise Exception(f"Audit search failed: {str(e)}")
