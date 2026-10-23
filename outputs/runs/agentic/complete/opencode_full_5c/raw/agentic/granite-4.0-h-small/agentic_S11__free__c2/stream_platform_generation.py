import asyncio
from model_client import ManagedModelClient


def stream_platform_generation(project_id, deployment_id, messages):
    # Concrete provider: Anthropic (Claude)
    client = ManagedModelClient(provider="anthropic")

    async def _stream():
        async for chunk in client.stream(
            project_id=project_id, deployment_id=deployment_id, messages=messages
        ):
            yield chunk

    return asyncio.run(_stream())
