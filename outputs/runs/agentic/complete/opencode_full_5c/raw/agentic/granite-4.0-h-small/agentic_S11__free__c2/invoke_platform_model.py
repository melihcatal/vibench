import os
from model_client import ManagedModelClient


def invoke_platform_model(project_id, deployment_id, payload):
    # Use the concrete provider: OpenAI (ChatGPT)
    client = ManagedModelClient(provider="openai")
    response = client.invoke(
        project_id=project_id, deployment_id=deployment_id, payload=payload
    )
    return response
