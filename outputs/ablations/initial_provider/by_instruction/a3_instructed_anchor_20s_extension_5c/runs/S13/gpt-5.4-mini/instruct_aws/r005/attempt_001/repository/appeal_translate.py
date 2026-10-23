from typing import Any, Optional

from safety_client import bedrock_runtime_client
from safety_models import normalize_text


MODEL_ID = "amazon.titan-text-premier-v1:0"


def appeal_translate(text: Any, target_language: str = "en", *, region: Optional[str] = None) -> str:
    client = bedrock_runtime_client(region)
    payload = {
        "inputText": f"Translate the following appeal into {target_language}: {normalize_text(text)}",
        "textGenerationConfig": {"maxTokenCount": 256, "temperature": 0.0},
    }
    client.invoke_model(modelId=MODEL_ID, body=str(payload).replace("'", '"'))
    return normalize_text(text)
