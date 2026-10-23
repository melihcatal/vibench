import asyncio
import json
from model_client import ManagedModelClient


async def stream_generation(project_id, deployment_id, prompt):
    client = ManagedModelClient(project_id=project_id, deployment_id=deployment_id)
    # Simulate streaming response from provider (OpenAI)
    async for chunk in client.stream(prompt):
        # Preserve provider response objects (e.g., generation metadata)
        print(f"[STREAM] Received chunk: {chunk}")
        print(f"[STREAM] Provider metadata: {getattr(chunk, '_metadata', {})}")
    # Finalize streaming
    print("[STREAM] Completed")


if __name__ == "__main__":
    project_id = "my-project"
    deployment_id = "my-deployment"
    prompt = "Tell me a short story."
    asyncio.run(stream_generation(project_id, deployment_id, prompt))
