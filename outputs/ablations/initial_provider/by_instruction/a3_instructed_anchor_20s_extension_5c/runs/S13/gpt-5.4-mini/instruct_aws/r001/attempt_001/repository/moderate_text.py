import json
from typing import Any, Dict

from safety_client import bedrock_runtime_client, load_model_id
from safety_models import SafetyDecision, SafetyRequest, normalize_text, normalize_thresholds


DEFAULT_MODEL_ID = "amazon.titan-text-express-v1"


def moderate_text(text: str, thresholds: Dict[str, Any] | None = None) -> SafetyDecision:
    request = SafetyRequest(text=normalize_text(text), thresholds=normalize_thresholds(thresholds))
    client = bedrock_runtime_client()
    model_id = load_model_id(DEFAULT_MODEL_ID)
    prompt = {
        "inputText": request.text,
        "textGenerationConfig": {"maxTokenCount": 16, "temperature": 0.0, "topP": 1.0},
    }
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(prompt).encode("utf-8"),
    )
    raw = json.loads(response["body"].read().decode("utf-8"))
    score = float(raw.get("score", 0.0))
    category = str(raw.get("category", "general"))
    threshold = request.thresholds.get(category, request.thresholds.get("default", 0.5))
    allowed = score < threshold
    return SafetyDecision(allowed=allowed, category=category, score=score, provider="aws-bedrock", raw=raw)
