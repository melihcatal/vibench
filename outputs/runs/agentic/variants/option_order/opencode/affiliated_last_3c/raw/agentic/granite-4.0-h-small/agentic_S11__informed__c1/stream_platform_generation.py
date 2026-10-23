import json
from model_client import ManagedModelClient
from model_models import Model


def stream_generation(
    model: Model,
    messages: list,
) -> dict:
    """Stream output from a managed model while preserving full provider responses.

    Args:
        model: Model instance representing the target deployment/model.
        messages: Prompt messages in provider‑specific format (e.g., OpenAI list of dicts).

    Returns:
        dict: Normalized response with streamed `output` chunks and optional metadata.
    """
    client = ManagedModelClient()
    response = client._client.chat.completions.create(
        project=model.provider,  # Azure OpenAI requires the resource name
        deployment=model.deployment or model.model_id,
        messages=messages,
        stream=True,
    )
    streamed_output: list[str] = []
    for chunk in response:
        # Each chunk has a `choices[0].delta.content` field; concatenate as strings
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        streamed_output.append(delta)
    normalized = {
        "output": "".join(streamed_output),
        "metadata": {
            "provider": client.PROVIDER,
            "model_id": model.model_id,
            "deployment": model.deployment or model.model_id,
        },
        "raw": response,
    }
    return normalized
