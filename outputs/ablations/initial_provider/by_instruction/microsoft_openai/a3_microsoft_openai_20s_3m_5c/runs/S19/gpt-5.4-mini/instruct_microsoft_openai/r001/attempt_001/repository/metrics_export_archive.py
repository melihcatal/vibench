import json
from typing import Any, Dict

from observability_client import create_openai_client, client_model_name, build_chat_messages


def metrics_export_archive(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    client = create_openai_client()
    model = client_model_name()
    response = client.chat.completions.create(model=model, messages=build_chat_messages("You archive managed metric snapshots.", json.dumps(snapshot)))
    return {"archived": True, "details": response.choices[0].message.content if response.choices else "", "provider": "openai", "model": model}
