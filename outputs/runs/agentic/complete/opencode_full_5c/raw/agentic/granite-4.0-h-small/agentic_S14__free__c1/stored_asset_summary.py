# stored_asset_summary.py
# [LATER-STEP] Summarize content extracted from a stored asset
# Using OpenAI GPT-4o as the concrete LLM provider (via OpenAI SDK)
import os
import openai
from storage_models import ObjectMetadataResponse, DownloadResponse

openai.api_key = os.getenv('OPENAI_API_KEY', '')
client = openai.OpenAI()

def summarize_asset(metadata: ObjectMetadataResponse, document_key: str) -> str:
    """Generate a concise summary of an asset using its metadata and extracted text.

    The function assumes external helper `download_document_text` provides plain text.
    Here we simulate by directly calling the OpenAI chat completion.
    """
    # Placeholder for extracted text - in real use you'd call a PDF/image parser first
    extracted_text = "This is the full text of the stored document. It covers various topics including architecture, implementation details, and user guidelines."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize the following document in 2-3 sentences:\n\n{extracted_text}\n\nMetadata: {metadata}"]},
    )
    return response.choices[0].message.content
