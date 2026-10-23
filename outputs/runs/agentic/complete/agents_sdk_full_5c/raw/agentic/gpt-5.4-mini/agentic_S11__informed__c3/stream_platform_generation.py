from __future__ import annotations

import json
from typing import Dict, Iterator

from model_client import bedrock_runtime_client, load_config
from model_models import PlatformRequest



def stream_platform_generation(request: PlatformRequest) -> Iterator[Dict[str, object]]:
    config = load_config()
    client = bedrock_runtime_client()
    response = client.converse_stream(
        modelId=config.bedrock_model_id,
        messages=[{"role": "user", "content": [{"text": request.prompt}]}],
        inferenceConfig={"maxTokens": request.max_tokens, "temperature": request.temperature},
    )
    yield {"provider": "Amazon Bedrock", "response": response}
    for event in response["stream"]:
        yield event
