# model_models.py
"""Define local request, response, and normalization helpers for Managed Model Platform Workflow.
These dataclasses wrap provider-specific payloads so higher‑level modules can work with provider‑agnostic objects.
"""

from dataclasses import dataclass
from typing import List, Dict, Any

class ProviderInfo:
    """Metadata supplied by the concrete provider (e.g., Bedrock) alongside generated text."""
    requestId: str
    usage: Dict[str, int]  # e.g., {\"promptTokens\": 12, \"completionTokens\": 34}
    modelId: str

class ApiResponse:
    """Normalized response container used by other workflow modules."""
    text: str
    provider_info: ProviderInfo

def normalize_bedrock_response(raw: dict) -> ApiResponse:
    """Convert Bedrock runtime raw dict into the generic ApiResponse."""
    provider_info = ProviderInfo(
        requestId=raw.get('requestId', '' ),
        usage=raw.get('usage', {}),
        modelId=raw.get('modelId', '')
    )
    # Assume Bedrock returns a list of chunks under 'generatedTextChunks'
    # The real API may differ; adjust accordingly.
    text = ''.join(chunk.get('text', '') for chunk in raw.get('generatedTextChunks', []))
    return ApiResponse(text=text, provider_info=provider_info)
