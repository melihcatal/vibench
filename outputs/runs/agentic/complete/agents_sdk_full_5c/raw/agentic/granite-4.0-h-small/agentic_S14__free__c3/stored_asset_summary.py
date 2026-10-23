'''Summarize content extracted from an Azure Blob using OpenAI embeddings.'''
import os
import openai
from typing import Dict
from storage_client import get_blob_service_client
from storage_models import ObjectMetadataResult, UploadResult
from pathlib import Path

def stored_asset_summary(container_name: str, blob_name: str) -> Dict[str, str]:
    """Generate a concise summary for the content of a stored Azure Blob.
    
    Steps:
    1. Download blob content (assumes plain text or PDF; for PDF you would add PDF parsing).
    2. Split content into chunks and embed each chunk using OpenAI's embeddings API.
    3. Use OpenAI's chat completion to ask for a summary of the whole content.
    
    Returns a dict with 'summary' field.
    """
    # 1. Download blob
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    content = blob_client.download_blob().readall().decode('utf-8')
    # simple chunking (for demo purposes)
    chunk_size = 1000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    # 2. Embed chunks
    embeddings = openai.Embeddings.create(input=chunks, model='text-embedding-ada-002')
    vectors = [entry['embedding'] for entry in embeddings['data']]
    # 3. Summarize with chat completion
    system_prompt = "You are a helpful assistant that summarizes long documents concisely."
    user_prompt = "Summarize the following document:\n\n" + "\n\n".join(chunks)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    summary = response['choices'][0]['message']['content']
    return {'summary': summary}
