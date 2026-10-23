from typing import Dict, List
from model_client import get_azure_openai_client
from model_models import GenerationRequest, chunk_delta_text
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: GenerationRequest) -> Dict[str, List[object]]:
    resource = select_platform_resource(request)
    client = get_azure_openai_client()
    stream = client.chat.completions.create(
        model=resource.azure_deployment,
        messages=request.to_chat_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    chunks = []
    parts = []
    for chunk in stream:
        chunks.append(chunk)
        text = chunk_delta_text(chunk)
        if text:
            parts.append(text)
    return {
        "text_parts": parts,
        "provider_chunks": chunks,
    }
