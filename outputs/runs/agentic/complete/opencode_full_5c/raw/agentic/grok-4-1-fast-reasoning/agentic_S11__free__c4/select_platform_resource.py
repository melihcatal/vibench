import os


def select_platform_resource(model_family: str) -> str:
    deployment_map = {
        "gpt-4o": os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT", "gpt-4o"),
        "gpt-4o-mini": os.getenv("AZURE_OPENAI_GPT4O_MINI_DEPLOYMENT", "gpt-4o-mini"),
        "gpt-4-turbo": os.getenv("AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT", "gpt-4-turbo"),
    }
    return deployment_map.get(model_family, model_family)
