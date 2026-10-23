from typing import Any, Dict, List, Optional

from openai import OpenAI

from safety_client import get_openai_client, moderation_model_name
from safety_models import normalize_moderation_result, normalize_batch_input


def moderate_batch(messages: List[str], user_id: Optional[str] = None) -> Dict[str, Any]:
    client = get_openai_client()
    model = moderation_model_name()
    normalized_messages = normalize_batch_input(messages)
    items: List[Dict[str, Any]] = []
    for idx, message in enumerate(normalized_messages):
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are a text safety moderation engine. Return structured JSON with allow/deny decision, categories, and rationale for one message.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text={"format": {"type": "json_object"}},
            metadata={"user_id": user_id, "batch_index": idx} if user_id else {"batch_index": idx},
        )
        items.append({"index": idx, "message": message, "result": normalize_moderation_result(response.output_text)})
    return {"results": items}
