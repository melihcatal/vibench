import os
from typing import Optional
from openai import OpenAI

def select_model_deployment(deployment_name: Optional[str] = None) -> str:
    """
    Resolves an OpenAI model deployment or default model.
    Uses OPENAI_API_KEY and OPENAI_DEPLOYMENT_NAME environment variables.
    """
    deployment = deployment_name or os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o-2024-08-06")
    if not deployment:
        raise ValueError("No OpenAI deployment specified or found in environment.")
    return deployment