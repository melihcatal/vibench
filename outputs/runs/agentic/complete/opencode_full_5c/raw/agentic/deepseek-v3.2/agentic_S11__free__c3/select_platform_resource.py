import os
from openai import OpenAI
from model_client import get_openai_client


def select_platform_resource(
    task_type: str = "general", max_tokens: int = 4000, streaming: bool = False
) -> str:
    """
    Resolve a provider-specific OpenAI model based on task requirements.
    """
    client = get_openai_client()

    # Map task types to appropriate OpenAI models
    model_map = {
        "general": "gpt-4o",
        "creative": "gpt-4o",
        "analysis": "gpt-4o",
        "coding": "gpt-4o",
        "reasoning": "gpt-4-turbo",
        "long_context": "gpt-4o-2024-08-06",
        "cheap": "gpt-3.5-turbo",
    }

    # Select model based on task type
    model_id = model_map.get(task_type, "gpt-4o")

    # Adjust model based on token requirements
    if max_tokens > 16000 and model_id == "gpt-4o":
        model_id = "gpt-4o-2024-08-06"

    # Check if model is available
    try:
        # Test model availability by making a simple request
        test_response = client.models.retrieve(model_id)
        if test_response.id:
            print(f"Selected OpenAI model: {model_id} for {task_type} task")
            return model_id
    except Exception:
        # Fallback to a known available model
        print(f"Model {model_id} not available, falling back to gpt-4o")
        return "gpt-4o"

    return model_id
