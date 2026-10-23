from model_client import get_deployment

def select_platform_resource(task_type: str) -> str:
    model_families = {
        "chat": "gpt-4o",
        "summarize": "gpt-4o-mini",
        "default": "gpt-4o-mini"
    }
    model_family = model_families.get(task_type, "default")
    return get_deployment(model_family)
