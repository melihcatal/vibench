# Embed object metadata and extracted text for search (AWS OpenSearch / BM25 or Pinecone example)
import os
from storage_client import create_s3_client
import boto3
import hashlib

# Placeholder: replace with actual OpenSearch endpoint and credentials
eop_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
OPENSEARCH_REGION = os.getenv("OPENSEARCH_REGION", "us-east-1")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "asset-store")


def embed_metadata(bucket: str, key: str):
    """Push a document record containing metadata and extracted text to an embeddings store."""
    client = create_s3_client()
    obj = client.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")

    # Simple embedding: SHA256 of the content (replace with real embedding model if needed)
    embedding = hashlib.sha256(content.encode("utf-8")).hexdigest()

    # Build a searchable document
    document = {
        "id": f"{bucket}/{key}",
        "metadata": {  # raw S3 metadata fields
            "bucket": bucket,
            "key": key,
            "size": obj["ContentLength"],
            "last_modified": str(obj["LastModified"]),
        },
        "text": content,  # full text for BM25 search
        "embedding": embedding,  # simple placeholder embedding
        "source": "managed-object-storage",
    }

    # Index into OpenSearch (or any vector DB)
    os_client = boto3.client("opensearch", region_name=OPENSEARCH_REGION)
    os_client.index(Index=OPENSEARCH_INDEX, Id=document["id"], Body=document)
    return f"Indexed {document['id']} into {OPENSEARCH_INDEX}"
