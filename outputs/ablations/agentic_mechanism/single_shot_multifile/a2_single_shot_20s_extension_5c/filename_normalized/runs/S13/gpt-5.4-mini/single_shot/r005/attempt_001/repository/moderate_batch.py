from typing import Any, Dict, Iterable, List, Optional
from safety_client import build_openai_client, provider_name
from safety_models import build_batch_result, extract_moderation_output

MODEL = "omni-moderation-latest"


def moderate_batch(messages: Iterable[str], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    items: List[Dict[str, Any]] = []
    for index, message in enumerate(messages):
        response = client.moderations.create(model=MODEL, input=message)
        parsed = extract_moderation_output(response)
        items.append(
            {
                "index": index,
                "text": message,
                "provider": provider_name(),
                "model": MODEL,
                "moderation": parsed,
            }
        )
    return build_batch_result(provider=provider_name(), operation="moderate_batch", items=items, metadata=metadata)
