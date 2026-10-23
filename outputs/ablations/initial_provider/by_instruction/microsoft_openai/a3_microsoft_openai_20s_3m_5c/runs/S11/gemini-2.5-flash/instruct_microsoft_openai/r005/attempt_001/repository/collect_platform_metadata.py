import os
from openai import AzureOpenAI
from typing import Dict, Any

def collect_platform_metadata(prompt: str, deployment_id: str) -> Dict[str, Any]:
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        logprobs=False  # Request logprobs to get more metadata if desired
    )

    # Extract content
    model_output = response.choices[0].message.content

    # Extract metadata
    metadata = {
        "id": response.id,
        "model": response.model,
        "created": response.created,
        "usage": response.usage.model_dump() if response.usage else None,  # Token usage
        "finish_reason": response.choices[0].finish_reason,
    }

    return {"output": model_output, "metadata": metadata}
