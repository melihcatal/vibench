def select_platform_resource(model_hint: str) -> str:
    deployment_map = {
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o",
        "gpt-35-turbo": "gpt-35-turbo",
    }
    return deployment_map.get(model_hint, model_hint)
