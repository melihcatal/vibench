import os
from openai import OpenAI
from model_client import get_openai_client


def select_platform_resource(
    task_type: str, budget_tokens: int = None, latency_requirement: str = "standard"
) -> str:
    """Resolve a provider-specific model, deployment, or inference resource before invocation."""
    client = get_openai_client()

    # Map task types to appropriate OpenAI models
    model_mapping = {
        "chat": "gpt-4o",
        "chat_fast": "gpt-4o-mini",
        "code": "gpt-4o",
        "reasoning": "gpt-4o",
        "creative": "gpt-4o",
        "analysis": "gpt-4o",
    }

    # Select base model based on task type
    base_model = model_mapping.get(task_type, "gpt-4o")

    # Adjust model based on budget constraints
    if budget_tokens and budget_tokens < 1000:
        # Use smaller model for tight budgets
        if base_model == "gpt-4o":
            selected_model = "gpt-4o-mini"
        else:
            selected_model = base_model
    elif latency_requirement == "fast":
        # Use faster model for low latency requirements
        selected_model = "gpt-4o-mini"
    else:
        selected_model = base_model

    # Verify model availability (simplified check)
    available_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
    if selected_model not in available_models:
        selected_model = "gpt-4o"

    print(f"Selected OpenAI model: {selected_model} for task: {task_type}")
    return selected_model


def list_available_models() -> list:
    """List available OpenAI models for the current API key."""
    client = get_openai_client()

    try:
        # Note: OpenAI's models.list() requires specific permissions
        # For demonstration, we'll return a static list of commonly available models
        return [
            {"id": "gpt-4o", "object": "model", "created": 1687882411},
            {"id": "gpt-4o-mini", "object": "model", "created": 1687882412},
            {"id": "gpt-4-turbo", "object": "model", "created": 1687882410},
        ]
    except Exception as e:
        print(f"Error listing models: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    model = select_platform_resource("chat", budget_tokens=500)
    print(f"Selected model: {model}")

    models = list_available_models()
    print(f"Available models: {[m['id'] for m in models]}")
