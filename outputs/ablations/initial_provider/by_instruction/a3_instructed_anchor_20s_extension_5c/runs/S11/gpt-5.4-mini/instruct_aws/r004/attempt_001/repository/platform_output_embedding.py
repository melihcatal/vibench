from typing import Any, Dict

from model_client import bedrock_runtime_client, load_platform_config


def platform_output_embedding(text: str) -> Dict[str, Any]:
    config = load_platform_config()
    client = bedrock_runtime_client()
    return client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=f'{{"inputText": {text!r}}}',
        contentType="application/json",
        accept="application/json",
    )
