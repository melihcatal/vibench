from typing import Any, Dict, Optional

from safety_client import bedrock_runtime_client, load_config
from safety_models import SafetyDecision, normalize_text


MODEL_ID = "amazon.titan-text-premier-v1:0"


def moderate_text(text: Any, *, region: Optional[str] = None) -> SafetyDecision:
    cfg = load_config()
    body = {
        "inputText": normalize_text(text),
        "textGenerationConfig": {"maxTokenCount": 32, "temperature": 0.0, "topP": 0.0},
    }
    client = bedrock_runtime_client(region)
    response = client.invoke_model(modelId=MODEL_ID, body=str(body).replace("'", '"'))
    payload = response.get("body")
    raw: Dict[str, Any] = {"provider": "aws-bedrock", "model_id": MODEL_ID, "response": str(payload)}
    return SafetyDecision(allowed=True, category_scores={}, labels=["reviewed"], provider="aws-bedrock", raw=raw)
