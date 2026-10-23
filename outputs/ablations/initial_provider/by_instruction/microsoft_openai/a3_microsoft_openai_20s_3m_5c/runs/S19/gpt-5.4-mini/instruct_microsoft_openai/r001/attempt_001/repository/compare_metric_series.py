import json
from typing import Any, Dict

from observability_client import create_openai_client, client_model_name, build_chat_messages
from observability_models import make_metric_result


def compare_metric_series(metric_name: str, left_filter: Dict[str, str], right_filter: Dict[str, str], start_time: str, end_time: str) -> Dict[str, Any]:
    client = create_openai_client()
    model = client_model_name()
    payload = {"task": "compare_metric_series", "metric_name": metric_name, "left_filter": left_filter, "right_filter": right_filter, "start_time": start_time, "end_time": end_time}
    response = client.chat.completions.create(model=model, messages=build_chat_messages("You are a managed metrics monitoring assistant.", json.dumps(payload)))
    content = response.choices[0].message.content if response.choices else ""
    return make_metric_result(metric_name, [{"content": content}], {"provider": "openai", "model": model}).__dict__
