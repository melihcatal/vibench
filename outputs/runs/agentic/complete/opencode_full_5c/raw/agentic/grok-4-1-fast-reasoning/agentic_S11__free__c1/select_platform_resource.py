import os


def select_platform_resource(model_hint: str) -> str:
    """
    Resolves a provider-specific deployment resource for Azure OpenAI.
    """
    deployments = {
        "gpt-4o-mini": os.getenv(
            "AZURE_GPT4O_MINI_DEPLOYMENT_ID", "gpt-4o-mini-deployment"
        ),
    }
    return deployments.get(model_hint, model_hint)
