from typing import Any, Optional

from safety_client import bedrock_runtime_client
from safety_models import normalize_text


MODEL_ID = "amazon.nova-lite-v1:0"


def reviewer_brief_audio(text: Any, *, region: Optional[str] = None) -> bytes:
    client = bedrock_runtime_client(region)
    payload = {"inputText": f"Create a spoken moderation brief: {normalize_text(text)}"}
    client.invoke_model(modelId=MODEL_ID, body=str(payload).replace("'", '"'))
    return b""
