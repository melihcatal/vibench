from model_client import build_platform_client


def select_platform_resource(model_name: str = "gpt-5.4-mini") -> str:
    client = build_platform_client()
    models = client.models.list()
    for item in models.data:
        if item.id == model_name:
            return item.id
    return models.data[0].id
