# stored_asset_summary.py
import os
from storage_client import ManagedStorageClient
from storage_models import SummaryResponse
from openai import OpenAI  # concrete provider SDK import signal

# Configure the provider client (e.g., via env var OPENAI_API_KEY)
openai_client = OpenAI()

def summarize_stored_asset(bucket: str, object_key: str, model: str = "gpt-4o-mini") -> SummaryResponse:
    """Generate a concise summary of content extracted from a stored asset using a hosted LLM.

    Args:
        bucket: Bucket/container name.
        object_key: Path to the asset file.
        model: Identifier for the hosted model family.

    Returns:
        SummaryResponse containing the AI-generated summary.
    """
    client = ManagedStorageClient()
    # Retrieve the asset (text or document) as raw bytes
    object_bytes = client.download(bucket, object_key)
    try:
        # Attempt to interpret as UTF-8 text; fallback to binary-to-text extraction if needed
        content = object_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback: extract printable characters
        content = ''.join(ch for ch in object_bytes if ch.isprintable())

    # Call the hosted LLM summarization endpoint
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': f"Summarize this content in three sentences:\n\n{content}"}],
        temperature=0.2,
    )
    summary = response.choices[0].message.content.strip()
    return SummaryResponse(summary=summary)
