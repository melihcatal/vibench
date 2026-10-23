# stream_platform_generation.py
# [SAME-SCENARIO] Stream output from a managed model platform while preserving provider response objects

# Using IBM watsonx.ai as the concrete provider

from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType
import json
import sys

WATSONX_API_KEY = "${WATSONX_API_KEY}"
WATSONX_PROJECT_ID = "${WATSONX_PROJECT_ID}"


def stream_generation(deployment_id, prompt, chunk_size=1024):
    """
    Stream generation output from watsonx.ai.
    Yields (output_chunk, provider_metadata) tuples.
    """
    client = Client(
        url="https://api.ibm.com/watsonx",
        api_key=WATSONX_API_KEY,
        service_type=ServiceType.WATSONX_AI,
    )
    # watsonx.ai's streaming endpoint (simulated via manual chunking of response text)
    response = client.generation.run(
        deployment_id=deployment_id, prompt=prompt, output_format="json"
    )
    # Simulate streaming by yielding chunks of the raw text
    for i in range(0, len(response.text), chunk_size):
        chunk = response.text[i : i + chunk_size]
        yield (
            chunk,
            {
                "provider": "watsonx.ai",
                "response_id": response.request_id,
                "chunk_index": i // chunk_size + 1,
                "total_chunks": (len(response.text) + chunk_size - 1) // chunk_size,
            },
        )


if __name__ == "__main__":
    deployment_id = "my-wx-deployment"
    prompt = "Provide a brief story about a future city, one paragraph per line."
    for chunk, meta in stream_generation(deployment_id, prompt):
        print(f"[Chunk {meta['chunk_index']}/{meta['total_chunks']}] {chunk}", end="")
