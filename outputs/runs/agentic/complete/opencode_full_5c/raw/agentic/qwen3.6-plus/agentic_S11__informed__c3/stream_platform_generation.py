from typing import Optional

from dashscope import Generation

from model_client import configure_dashscope_client, create_generation_request
from model_models import ModelRequest, StreamChunk, extract_request_id


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
):
    configure_dashscope_client(api_key)

    request = ModelRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    params = create_generation_request(request)
    responses = Generation.call(**params, stream=True, incremental_output=True)

    full_text = ""
    chunk_index = 0
    request_id = None

    for response in responses:
        if request_id is None:
            request_id = extract_request_id(response)

        if hasattr(response, "output") and isinstance(response.output, dict):
            text = response.output.get("text", "")
            finish_reason = response.output.get("finish_reason")
        elif isinstance(response, dict):
            text = response.get("output", {}).get("text", "")
            finish_reason = response.get("output", {}).get("finish_reason")
        else:
            text = str(response)
            finish_reason = None

        if text:
            full_text += text
            chunk = StreamChunk(
                text=text,
                index=chunk_index,
                finish_reason=finish_reason,
                raw_chunk=response,
            )
            chunk_index += 1
            yield chunk
