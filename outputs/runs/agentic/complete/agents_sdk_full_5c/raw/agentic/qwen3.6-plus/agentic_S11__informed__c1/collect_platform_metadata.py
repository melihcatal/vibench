"""Return model output together with provider platform metadata from Azure OpenAI.

Uses Azure OpenAI Service (sdk=openai) with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY.
Collects usage token counts, model handles, deployment IDs, and content filter results.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from openai import AzureOpenAI

from model_client import create_azure_openai_client, get_default_deployment
from model_models import ModelRequest, PlatformMetadata, ModelResponse


@dataclass
class EnrichedResponse:
    """Model output enriched with full Azure OpenAI platform metadata."""

    text: str
    finish_reason: str
    metadata: PlatformMetadata
    deployment_name: str
    model_family: str
    request_id: str
    system_fingerprint: str = ""


def _extract_model_family(model_identifier: str) -> str:
    """Derive the Azure OpenAI model family from the model identifier string."""
    lower = model_identifier.lower()
    if "gpt-4o" in lower:
        return "gpt-4o"
    elif "gpt-4" in lower:
        return "gpt-4"
    elif "gpt-35-turbo" in lower or "gpt-3.5" in lower:
        return "gpt-3.5-turbo"
    return lower


def _parse_content_filter(response: Any) -> dict[str, Any]:
    """Extract Azure AI content safety filter results from the response."""
    result: dict[str, Any] = {}
    choice = response.choices[0] if response.choices else None
    if choice and hasattr(choice, "content_filter_results"):
        cfr = choice.content_filter_results
        result = {
            "hate": cfr.hate.to_dict() if hasattr(cfr.hate, "to_dict") else str(cfr.hate),
            "self_harm": cfr.self_harm.to_dict() if hasattr(cfr.self_harm, "to_dict") else str(cfr.self_harm),
            "sexual": cfr.sexual.to_dict() if hasattr(cfr.sexual, "to_dict") else str(cfr.sexual),
            "violence": cfr.violence.to_dict() if hasattr(cfr.violence, "to_dict") else str(cfr.violence),
        }
    return result


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    deployment: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    client: Optional[AzureOpenAI] = None,
) -> EnrichedResponse:
    """Invoke Azure OpenAI and return output with full provider platform metadata.

    Retrieves the model response along with:
    - Token usage (prompt, completion, total)
    - Model identifier and family
    - Deployment name and resource handle
    - Request ID for Azure tracing
    - System fingerprint
    - Content filter evaluation results

    Args:
        prompt: User input text.
        system_prompt: Optional system-level instruction.
        deployment: Azure OpenAI deployment name (e.g., gpt-4o).
        temperature: Sampling temperature.
        max_tokens: Maximum completion tokens.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        EnrichedResponse with text, metadata, and Azure platform details.
    """
    resolved_client = client or create_azure_openai_client()
    resolved_deployment = deployment or get_default_deployment()

    request = ModelRequest(
        prompt=prompt,
        deployment=resolved_deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
        stream=False,
    )

    messages = request.to_openai_messages()

    raw_response = resolved_client.chat.completions.create(
        model=resolved_deployment,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=False,
    )

    choice = raw_response.choices[0] if raw_response.choices else None
    text = ""
    finish_reason = ""
    if choice and choice.message:
        text = choice.message.content or ""
        finish_reason = choice.finish_reason or ""

    usage = raw_response.usage
    metadata = PlatformMetadata(
        model=raw_response.model,
        usage_prompt_tokens=usage.prompt_tokens if usage else 0,
        usage_completion_tokens=usage.completion_tokens if usage else 0,
        usage_total_tokens=usage.total_tokens if usage else 0,
        request_id=getattr(raw_response, "id", ""),
        deployment_name=resolved_deployment,
        content_filter_result=_parse_content_filter(raw_response),
        raw_response=raw_response,
    )

    model_family = _extract_model_family(raw_response.model)
    system_fingerprint = getattr(raw_response, "system_fingerprint", "")

    return EnrichedResponse(
        text=text,
        finish_reason=finish_reason,
        metadata=metadata,
        deployment_name=resolved_deployment,
        model_family=model_family,
        request_id=getattr(raw_response, "id", ""),
        system_fingerprint=system_fingerprint,
    )


if __name__ == "__main__":
    enriched = collect_platform_metadata(
        prompt="What are the capital cities of France, Germany, and Japan?",
        system_prompt="Answer concisely.",
    )
    print(f"Text: {enriched.text}")
    print(f"Model: {enriched.metadata.model}")
    print(f"Family: {enriched.model_family}")
    print(f"Deployment: {enriched.deployment_name}")
    print(f"Request ID: {enriched.request_id}")
    print(f"Prompt tokens: {enriched.metadata.usage_prompt_tokens}")
    print(f"Completion tokens: {enriched.metadata.usage_completion_tokens}")
    print(f"Total tokens: {enriched.metadata.usage_total_tokens}")
