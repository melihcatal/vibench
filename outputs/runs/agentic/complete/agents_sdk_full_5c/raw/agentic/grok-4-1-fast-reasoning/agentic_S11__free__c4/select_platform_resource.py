from model_client import get_platform_client

def select_platform_resource(model_family: str = "gpt-4o-mini") -> str:
    client = get_platform_client()
    models = client.models.list()
    for model in models.data:
        if model_family.lower() in model.id.lower():
            return model.id
    available = [m.id for m in models.data]
    raise ValueError(f"No deployment for {model_family}. Available: {available}")
