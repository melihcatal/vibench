from openai import AzureOpenAI

from model_client import get_azure_openai_client
from model_models import ModelRequest


def platform_output_safety(request: ModelRequest) -> dict:
    client: AzureOpenAI = get_azure_openai_client()
    response = client.moderations.create(input=request.prompt)
    return response.model_dump() if hasattr(response, "model_dump") else {"raw": response}
