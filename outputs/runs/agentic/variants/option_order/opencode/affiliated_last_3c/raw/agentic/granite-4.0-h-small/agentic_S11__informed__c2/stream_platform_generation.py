import asyncio
import os
from huggingface_hub import HfApi


async def stream_platform_generation(
    model_id: str, prompt: str, stream_handler, deployment_id: str = None
) -> None:
    """Stream generation from a Hugging Face managed model.
    Calls the model stream endpoint and yields each chunk to the provided handler.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "Set HF_TOKEN environment variable with your Hugging Face API token"
        )
    api = HfApi(token=hf_token)
    if deployment_id:
        async for chunk in api.inference_stream(deployment_id, inputs={"text": prompt}):
            stream_handler(chunk)
    else:
        async for chunk in api.inference_stream(model_id, inputs={"text": prompt}):
            stream_handler(chunk)
