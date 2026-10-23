from safety_client import ComprehendSafetyClient
from safety_models import BatchTextModerationRequest, BatchTextModerationResponse
from typing import Dict, Any, List

def moderate_batch(payload: Dict[str, Any], config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    config = config or {}
    client = ComprehendSafetyClient(region_name=config.get("region", "us-east-1"))

    texts = [item["text"] for item in payload["messages"]]
    language_code = payload.get("language_code", "en")

    request = BatchTextModerationRequest(texts=texts, language_code=language_code)
    response = client.moderate_batch_text(request)

    # Convert BatchTextModerationResponse to the desired output format
    per_message_decisions = []
    for i, msg_results in enumerate(response.batch_results):
        # For simplicity, we are taking the first result (Toxicity) and its score
        # In a more complex scenario, you might have multiple categories per message
        score = msg_results.results[0].score if msg_results.results else 0.0
        is_unsafe = score > config.get("batch_toxicity_threshold", 0.5) # Example threshold
        per_message_decisions.append({"message_index": i, "is_unsafe": is_unsafe, "score": score})

    return per_message_decisions
