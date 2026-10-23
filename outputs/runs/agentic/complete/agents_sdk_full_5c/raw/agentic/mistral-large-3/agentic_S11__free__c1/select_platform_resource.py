from openai import OpenAI
from typing import Optional

def select_model_deployment(deployment_name: Optional[str] = None) -> str:
    client = OpenAI()
    if deployment_name:
        return deployment_name
    models = client.models.list()
    available = [m.id for m in models.data if "gpt-4o" in m.id]
    return available[0] if available else "gpt-4o-2024-08-06"