from typing import Optional, Dict, Any
import os
from huggingface_hub import list_models, ModelFilter
from model_client import get_model_client_config


def select_platform_resource(
    task_type: str,
    model_family: Optional[str] = None,
    quantization: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves a Hugging Face Inference API or Endpoint model based on task and filters.
    """
    config = get_model_client_config()
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        raise ValueError("HF_TOKEN environment variable not set")

    filter_kwargs = {"task": task_type}
    if model_family:
        filter_kwargs["library"] = model_family
    if quantization:
        filter_kwargs["quantization"] = quantization

    models = list_models(filter=ModelFilter(**filter_kwargs), token=api_token, limit=5)

    selected_model = next(models, None)
    if not selected_model:
        raise RuntimeError(f"No Hugging Face model found for task: {task_type}")

    return {
        "model_id": selected_model.id,
        "model_task": selected_model.task,
        "model_tags": selected_model.tags,
        "provider": "huggingface",
    }
