import os
import subprocess
import sys
from pathlib import Path
from model_client import ManagedModelClient
from model_models import InferenceRequest, InferenceResponse


def stream_generation(
    provider: str, prompt: str, config: dict
) -> tuple[list[InferenceResponse], dict]:
    """
    Streams generation output from a managed model platform while preserving the raw provider response objects.
    Uses the selected provider (Hugging Face, Bedrock, watsonx, etc.) and yields response chunks.
    Returns a tuple of (collected responses, provider_metadata).
    """
    client = ManagedModelClient(config)
    # Resolve provider-specific client class based on provider name
    if provider == "huggingface":
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise RuntimeError("HF_TOKEN environment variable not set")
        from huggingface_hub import InferenceApi

        api = InferenceApi(repo_id=client.model_id, token=hf_token)
        responses = []
        iterator = api.pipe(prompt, stream=True)
        for chunk in iterator:
            # chunk is a dict representing the model output chunk
            responses.append(
                InferenceResponse(text=chunk.get("generated_text", ""), raw=chunk)
            )
            sys.stdout.write(chunk.get("generated_text", "") + "\n")
            sys.stdout.flush()
        provider_metadata = {
            "provider": "huggingface",
            "model_id": client.model_id,
            "request_id": getattr(iterator, "request_id", None),
        }
        return responses, provider_metadata
    elif provider == "bedrock":
        # AWS credentials assumed to be set in env
        import boto3
        from boto3.session import Session

        aws_profile = config.get("aws_profile", "default")
        session = Session(profile_name=aws_profile)
        bedrock = session.client(
            service_name="bedrock-runtime",
            region_name=config.get("region", "us-east-1"),
        )
        payload = {
            "contentType": "application/json",
            "accept": "application/json",
            "input": {"prompt": prompt, "maxTokens": 256},
        }
        resp = bedrock.post_generation(prompt=prompt)
        # Simplified streaming; Bedrock returns a single string response
        text = resp.get("body").read().decode()
        responses = [InferenceResponse(text=text, raw=resp)]
        provider_metadata = {"provider": "bedrock", "modelId": client.model_id}
        return responses, provider_metadata
    elif provider == "watsonx":
        # use ibm-watsonx-ai SDK
        from ibm_watsonx_ai import Client

        client_wx = Client(
            apikey=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        inference_api = client_wx.ai_runtime.InferenceJob.from_prompt(
            prompt, model_id=client.model_id
        )
        # Collect chunks (watsonx streaming not natively supported, simulate with list)
        responses = [
            InferenceResponse(
                text=inference_api.result.get("generated_text", ""),
                raw=inference_api.result,
            )
        ]
        provider_metadata = {"provider": "watsonx", "modelId": client.model_id}
        return responses, provider_metadata
    else:
        raise ValueError(f"Unsupported provider for streaming: {provider}")
