"""Invoke a provider-managed model through Azure OpenAI deployment-scoped platform client.

Uses Azure OpenAI Service (sdk=openai) with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY.
"""

from typing import Optional

from openai import AzureOpenAI

from model_client import create_azure_openai_client, get_default_deployment
from model_models import ModelRequest, ModelResponse, parse_azure_response


def invoke_platform_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    deployment: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    client: Optional[AzureOpenAI] = None,
) -> ModelResponse:
    """Invoke an Azure OpenAI deployment-scoped model and return a normalized response.

    Args:
        prompt: User input text.
        system_prompt: Optional system-level instruction.
        deployment: Azure OpenAI deployment name (e.g., gpt-4o).
        temperature: Sampling temperature.
        max_tokens: Maximum completion tokens.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        ModelResponse with text output and provider metadata.
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

    response = resolved_client.chat.completions.create(
        model=resolved_deployment,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=False,
    )

    return parse_azure_response(response)


if __name__ == "__main__":
    resp = invoke_platform_model(
        prompt="Explain the benefits of managed model platforms in three sentences.",
        system_prompt="You are a helpful AI assistant.",
    )
    print(resp.extract_text())
