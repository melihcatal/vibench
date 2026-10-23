import asyncio
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelStreamResponse

def stream_platform_generation(resource_id: str, prompt: str) -> None:
    """
    Stream real-time model output from a managed provider while preserving response objects.
    Args:
        resource_id: Provider-qualified model/deployment ID.
        prompt: Input text sent to the model.
    Yields:
        Tuples of (raw_response_object, text_chunk) as they arrive.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(resource_id=resource_id, prompt=prompt)
    async def _stream():
        # Many SDKs expose an async generator for streaming calls (e.g., OpenAI, Bedrock, Vertex)
        async for chunk in client.invoke_model_stream(request):
            yield chunk.raw_response, chunk.text
    asyncio.run(_stream())

#
# Simple CLI demo (uncomment to test)
# if __name__ == "__main__":
#     import sys
#     resource = os.getenv("MODEL_RESOURCE_ID")
#     text = os.getenv("PROMPT", "Generate a short story about a robot.")
#     print("Streaming model output...")
#     for resp, txt in stream_platform_generation(resource, text):
#         print(f"---chunk---\n{txt}", end="", flush=True)
