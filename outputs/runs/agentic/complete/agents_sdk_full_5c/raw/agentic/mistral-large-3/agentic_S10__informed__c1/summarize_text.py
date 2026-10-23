import os
from typing import Optional
from model_client import get_watsonx_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 200,
    temperature: float = 0.1,
    project_id: Optional[str] = None
) -> str:
    """
    Summarize long text using watsonx.ai Granite model.
    """
    client = get_watsonx_client()
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

    request = SummarizationRequest(
        model_id=model_id,
        input=text,
        parameters={
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "decoding_method": "greedy"
        }
    )

    response = client.text.generation.create(
        model_id=request.model_id,
        inputs=[request.input],
        parameters=request.parameters,
        project_id=project_id
    )

    return SummarizationResponse.from_watsonx(response).output