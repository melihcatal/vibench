def select_platform_resource(resource_type: str) -> str:
    # Azure OpenAI deployment mapping
    deployments = {
        "fast": "gpt-4o-mini-deployment",
        "smart": "gpt-4o-deployment",
        "long-context": "gpt-4-deployment",
    }
    return deployments.get(resource_type, "gpt-4o-mini-deployment")