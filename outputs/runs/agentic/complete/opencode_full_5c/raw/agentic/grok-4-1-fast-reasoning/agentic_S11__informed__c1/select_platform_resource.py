DEPLOYMENTS = {
    "gpt-4o-mini": "gpt-4o-mini-deployment",
    "gpt-4o": "gpt-4o-deployment",
}


def select_platform_resource(model_name: str) -> str:
    return DEPLOYMENTS.get(model_name, model_name)
