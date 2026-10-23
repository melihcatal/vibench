"""Return model output together with OpenAI provider platform metadata such as usage, resource IDs, or model handles.

Calls the OpenAI chat.completions endpoint and wraps the ChatCompletion
response in a PlatformMetadataEnvelope that exposes usage statistics,
response IDs, system fingerprints, and the raw provider object.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion

from model_client import create_openai_client, resolve_deployment_model, with_retry
from model_models import PlatformMetadataEnvelope, PlatformModelRequest


def collect_platform_metadata(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> PlatformMetadataEnvelope:
    """Invoke the OpenAI platform and return output with full metadata envelope.

    Returns a PlatformMetadataEnvelope containing:
      - The normalized model output (PlatformModelResponse)
      - The OpenAI response ID
      - The OpenAI system_fingerprint
      - Token usage statistics (prompt, completion, total)
      - The raw openai.ChatCompletion object
    """
    resolved_client = client or create_openai_client()
    payload = request.to_openai_payload()
    payload["stream"] = False

    def _call() -> ChatCompletion:
        return resolved_client.chat.completions.create(**payload)

    completion: ChatCompletion = with_retry(_call)
    return PlatformMetadataEnvelope.from_openai(completion)


def collect_platform_metadata_dict(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """Return a serializable dictionary of model output and OpenAI metadata."""
    envelope = collect_platform_metadata(request, client)
    data = {
        "platform": envelope.platform,
        "output": envelope.response.to_dict(),
        "request_id": envelope.request_id,
        "system_fingerprint": envelope.system_fingerprint,
    }
    if envelope.response.raw_response and envelope.response.raw_response.usage:
        usage = envelope.response.raw_response.usage
        data["usage"] = {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }
    return data
