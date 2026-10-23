import os
from openai import OpenAI


def get_openai_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )


def resolve_model_name(model: str = None):
    return model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def resolve_deployment_id(deployment: str = None):
    return deployment or os.environ.get("OPENAI_DEPLOYMENT", "default")


def resolve_platform_resource(
    resource: str = None, model: str = None, deployment: str = None
):
    return resource or deployment or model or resolve_model_name(model)
