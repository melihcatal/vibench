def resolve_platform_resource(model_family: str) -> str:
    deployments = {
        "gpt-4o-mini": "gpt-4o-mini-deployment",
        "gpt-4o": "gpt-4o-deployment",
        "gpt-3.5-turbo": "gpt-35-turbo-deployment",
    }
    return deployments.get(model_family, "gpt-4o-mini-deployment")
