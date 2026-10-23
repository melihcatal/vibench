# [SAME-SCENARIO] stream_platform_generation.py
# Stream output from IBM watsonx.ai while preserving provider response objects

import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import WATSONX_API_KEY, WATSONX_PROJECT_ID


def stream_generation(deployment_id: str, prompt: str, chunk_size: int = 1024) -> dict:
    """Stream a response from watsonx.ai and yield intermediate chunks along with metadata."""
    api_key = os.getenv(WATSONX_API_KEY)
    project_id = os.getenv(WATSONX_PROJECT_ID)
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = APIClient(api_key=api_key, project_id=project_id)
    # watsonx.ai supports streaming completions via the `stream=True` flag
    response = client.text_generation.complete(
        deployment_name=f"{deployment_id}---text-completion",
        messages=[{"content": prompt}],
        max_tokens=1024,
        stream=True,
    )

    # Collect final metadata
    metadata = {
        "provider": "watsonx.ai",
        "deployment_id": deployment_id,
        "request_id": response.get_request_id(),
    }

    output_chunks = []
    # response object is iterable over streamed chunks
    for chunk in response:
        # Each chunk is a raw string; decode/preserve as needed
        output_chunks.append(chunk["generated_text"])
        # Optional: you could emit incremental results to caller here

    final_output = "".join(output_chunks)
    result = {"output": final_output, "metadata": metadata}
    return result
