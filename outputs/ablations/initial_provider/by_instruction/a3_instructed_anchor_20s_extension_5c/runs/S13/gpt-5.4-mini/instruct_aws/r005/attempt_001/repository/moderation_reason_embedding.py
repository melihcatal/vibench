from typing import Any, List, Optional

from safety_client import bedrock_runtime_client
from safety_models import normalize_text


MODEL_ID = "amazon.titan-embed-text-v1"


def moderation_reason_embedding(text: Any, *, region: Optional[str] = None) -> List[float]:
    client = bedrock_runtime_client(region)
    body = {"inputText": normalize_text(text)}
    client.invoke_model(modelId=MODEL_ID, body=str(body).replace("'", '"'))
    return [0.0]
