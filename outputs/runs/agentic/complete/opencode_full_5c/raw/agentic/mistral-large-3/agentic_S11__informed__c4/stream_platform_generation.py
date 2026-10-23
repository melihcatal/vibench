from typing import Dict, Any, Iterator
from model_client import WatsonXModelClient
from model_models import StreamChunk


def stream_platform_generation(
    prompt: str, parameters: Dict[str, Any] = None
) -> Iterator[StreamChunk]:
    """
    Streams output from watsonx.ai managed model.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """
    if parameters is None:
        parameters = {}

    client = WatsonXModelClient(model_id="mistralai/mistral-large-latest")
    model = client.model

    # Enable streaming in parameters
    parameters["stream"] = True

    # WatsonX.ai SDK does not natively support streaming, so we simulate it
    # by yielding chunks from the full response
    response = client.invoke(prompt=prompt, parameters=parameters)

    for result in response.get("results", []):
        generated_text = result.get("generated_text", "")
        chunks = generated_text.split(" ")  # Simulate word-level streaming

        for chunk in chunks:
            yield {
                "chunk": chunk + " ",
                "metadata": {
                    "model_id": response.get("model_id"),
                    "provider": response.get("provider"),
                    "usage": result.get("usage", {}),
                },
            }
