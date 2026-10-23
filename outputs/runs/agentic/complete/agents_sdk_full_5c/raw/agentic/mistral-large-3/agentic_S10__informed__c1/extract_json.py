import json
import os
from typing import Dict, Any, Optional
from model_client import get_watsonx_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 500,
    temperature: float = 0.2,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using watsonx.ai Granite model.
    """
    client = get_watsonx_client()
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

    schema_str = json.dumps(schema)
    prompt = (
        f"Extract the following JSON structure from the text below. "
        f"Only respond with valid JSON matching this schema: {schema_str}\n\n"
        f"Text: {text}"
    )

    request = ExtractionRequest(
        model_id=model_id,
        input=prompt,
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

    output = ExtractionResponse.from_watsonx(response).output
    return json.loads(output)