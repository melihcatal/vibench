import os
from typing import Dict, Any
from model_client import get_azure_client
from model_models import ChatRequest, ChatResponse


def collect_platform_metadata(request: ChatRequest) -> Dict[str, Any]:
    """Return model output together with Azure OpenAI platform metadata."""
    client = get_azure_client()

    # Azure OpenAI specific deployment name
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    # Create Azure OpenAI chat completion request
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_message},
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False,
    )

    # Extract Azure OpenAI specific metadata
    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    # Collect Azure OpenAI platform metadata
    metadata = {
        "provider": "azure-openai",
        "deployment_name": deployment_name,
        "model_id": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens
            if response.usage
            else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        },
        "response_id": response.id,
        "created_timestamp": response.created,
        "finish_reason": finish_reason,
        "system_fingerprint": response.system_fingerprint,
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    }

    # Create response with metadata
    chat_response = ChatResponse(
        content=content, finish_reason=finish_reason, raw_response=response
    )

    return {"response": chat_response, "metadata": metadata}
