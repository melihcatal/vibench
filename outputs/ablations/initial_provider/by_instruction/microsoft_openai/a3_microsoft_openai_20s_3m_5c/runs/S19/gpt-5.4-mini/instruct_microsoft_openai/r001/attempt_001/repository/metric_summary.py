import json
from typing import Any, Dict

from observability_client import create_openai_client, client_model_name, build_chat_messages


def metric_summary(metric_name: str, points: Dict[str, Any]) -> Dict[str, Any]:
    client = create_openai_client()
    model = client_model_name()
    response = client.chat.completions.create(model=model, messages=build_chat_messages("You summarize managed metrics trends.", json.dumps({"metric_name": metric_name, "points": points})))
    return {"metric_name": metric_name, "summary": response.choices[0].message.content if response.choices else "", "provider": "openai", "model": model}
