from model_client import get_platform_client
import openai


def select_platform_resource() -> str:
    client = get_platform_client()
    models = client.models.list()
    for model_data in models.data:
        model_id = model_data.id
        if "gpt-4o" in model_id or "gpt-4" in model_id or "gpt-35" in model_id:
            return model_id
    # Fallback to default
    from model_client import get_default_deployment

    return get_default_deployment()
