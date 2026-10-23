'''Embed object metadata and extracted text for Azure Blob search.'''
import os
import openai
from typing import Dict
from storage_client import get_blob_service_client
from storage_models import ObjectMetadataResult
from pathlib import Path

def asset_metadata_embedding(container_name: str, blob_name: str) -> Dict[str, any]:
    """Create an embedding representation of metadata together with extracted plain-text content of a blob.

    Steps:
    1. Retrieve blob metadata.
    2. Download blob as raw text (assuming UTF-8 text file for demo; for other formats add conversion).
    3. Concatenate metadata strings and content to form a document.
    4. Send to OpenAI embeddings API (text-embedding-ada-002) and return the vector.

    Returns:
        Dictionary with keys: 'blob_name', 'container', 'embedding' (list of floats), 'metadata' (dict).
    """
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # 1. metadata
    metadata: ObjectMetadataResult = blob_client.get_blob_properties()
    meta_str = f"container: {container_name}\nblob: {blob_name}\nsize: {metadata.size}\nlast_modified: {metadata.last_modified}\ncontent_type: {metadata.content_type}\n"
    # 2. content (assume text)
    content = blob_client.download_blob().readall().decode('utf-8')
    document = meta_str + "\n\n" + content
    # 3. embed
    embedding_response = openai.Embeddings.create(input=document, model='text-embedding-ada-002')
    embedding = embedding_response['data'][0]['embedding']  # list of floats
    return {
        'blob_name': blob_name,
        'container': container_name,
        'embedding': embedding,
        'metadata': {
            'size': metadata.size,
            'last_modified': str(metadata.last_modified),
            'content_type': metadata.content_type,
            'etag': str(metadata.etag),
        },
    }
