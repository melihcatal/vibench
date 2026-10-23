import os
from openai import OpenAI


def select_platform_resource(task_type: str, budget_tier: str = "standard") -> str:
    """
    Resolves a provider-specific model, deployment, or inference resource before invocation.
    Selects appropriate OpenAI model based on task type and budget tier.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Map task types to appropriate OpenAI models
    model_mapping = {
        "chat": {
            "standard": "gpt-4o",
            "budget": "gpt-3.5-turbo",
            "advanced": "gpt-4-turbo",
        },
        "code": {
            "standard": "gpt-4o",
            "budget": "gpt-3.5-turbo",
            "advanced": "gpt-4-turbo",
        },
        "analysis": {
            "standard": "gpt-4o",
            "budget": "gpt-3.5-turbo",
            "advanced": "gpt-4-turbo",
        },
    }

    if task_type not in model_mapping:
        task_type = "chat"

    if budget_tier not in model_mapping[task_type]:
        budget_tier = "standard"

    selected_model = model_mapping[task_type][budget_tier]

    # Verify model availability by checking API
    try:
        models = client.models.list()
        available_models = [model.id for model in models.data]

        if selected_model not in available_models:
            # Fallback to a known available model
            if "gpt-4o" in available_models:
                selected_model = "gpt-4o"
            elif "gpt-3.5-turbo" in available_models:
                selected_model = "gpt-3.5-turbo"
            else:
                raise ValueError(f"Selected model {selected_model} not available")
    except Exception:
        # If model listing fails, proceed with selected model
        pass

    return selected_model
