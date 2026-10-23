import json
from typing import Any, Dict

from observability_client import create_openai_client, client_model_name, build_chat_messages
from observability_models import MetricWindowRequest, make_metric_result


def filter_metric_dimensions(metric_name: str, start_time: str, end_time: str, resource_filter: Dict[str, str]) -> Dict[str, Any]:
    request = MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=resource_filter)
    client = create_openai_client()
    model = client_model_name()
    response = client.chat.completions.create(model=model, messages=build_chat_messages("You are a managed metrics monitoring assistant.", json.dumps({"task": "filter_metric_dimensions", "request": request.__dict__})))
    content = response.choices[0].message.content if response.choices else ""
    return make_metric_result(metric_name, [{"content": content}], {"provider": "openai", "model": model}).__dict__
