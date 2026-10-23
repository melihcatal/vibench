import asyncio
import json
from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse

async def stream_provider(request: ModelRequest):
    """Stream generation from a managed model; yields raw response chunks."""
    client = ManagedModelClient(provider=request.config.get("provider", "anthropic"),
                                 api_key=os.getenv(request.config.get("provider", "anthropic") + "_API_KEY"))
    async for chunk in client.stream_chat(request.payload):
        # Each chunk is a provider-specific response object
        yield chunk

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are helpful.", "user": "Give me a short poem about stars."},
                            config={"provider": "anthropic"})
    async def run():
        async for part in stream_provider(demo_req):
            print(json.dumps(part.to_dict(), ensure_ascii=False))
    asyncio.run(run())
