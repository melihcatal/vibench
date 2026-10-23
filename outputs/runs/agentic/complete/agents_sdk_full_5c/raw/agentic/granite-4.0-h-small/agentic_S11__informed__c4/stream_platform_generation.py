import asyncio
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest

def stream_platform_generation() -> None:
    # Example using Vertex AI streaming generation (chat or text generation)
    async def _stream():
        async with ManagedModelClient() as client:
            request = ModelInvocationRequest(
                model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
                    os.getenv('GOOGLE_CLOUD_PROJECT'),
                    os.getenv('GCLOUD_LOCATION', 'us-central1')
                ),
                parameters={"temperature": 0.7, "max_output_tokens": 512},
                messages=[{"role": "user", "content": "Tell me a short story"}],
                stream=True,  # request streaming response
            )
            async for chunk in client.stream_generate(request):
                # chunk is provider-specific response object (e.g., VertexAIStreamingGenerateResponse)
                print('Streaming chunk:', chunk)
    asyncio.run(_stream())

if __name__ == '__main__':
    stream_platform_generation()
