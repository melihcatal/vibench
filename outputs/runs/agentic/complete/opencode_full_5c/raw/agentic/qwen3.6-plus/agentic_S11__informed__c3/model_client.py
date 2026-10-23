import os
from typing import Optional

import dashscope
from dashscope import Generation

from model_models import ModelRequest, build_messages, normalize_prompt


DASHSCOPE_DEFAULT_MODEL = "qwen-turbo"
DASHSCOPE_API_BASE = "dashscope.aliyuncs.com"


def get_dashscope_api_key() -> str:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")
    return api_key


def configure_dashscope_client(api_key: Optional[str] = None) -> None:
    key = api_key or get_dashscope_api_key()
    dashscope.api_key = key


def create_generation_request(
    request: ModelRequest,
    model_id: Optional[str] = None,
) -> dict:
    prompt = normalize_prompt(request.prompt)
    messages = build_messages(request.system_prompt, prompt)
    params: dict = {
        "model": model_id or request.model_id or DASHSCOPE_DEFAULT_MODEL,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
    }
    if request.stop_sequences:
        params["stop"] = request.stop_sequences
    params.update(request.extra_params)
    return params


def call_dashscope_sync(params: dict) -> Generation.Response:
    return Generation.call(**params)


def call_dashscope_stream(params: dict):
    return Generation.call(**params, stream=True, incremental_output=True)
