import os
from huggingface_hub import HfApi


def invoke_platform_model(
    model_id: str, prompt: str, deployment_id: str = None
) -> dict:
    """Invoke a Hugging Face managed model.
    model_id: model identifier (e.g., 'meta-llama/Meta-Llama-3-8B-Instruct')
    prompt: input text for the model
    deployment_id: optional deployment ID for a hosted inference endpoint
    Returns the raw provider response.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "Set HF_TOKEN environment variable with your Hugging Face API token"
        )
    api = HfApi(token=hf_token)
    if deployment_id:
        # Use deployment endpoint
        response = api.inference(deployment_id, inputs={"text": prompt})
    else:
        # Use model inference endpoint
        response = api.inference(model_id, inputs={"text": prompt})
    return response
