from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import openai

from model_client import OpenAIPlatformClient, get_platform_client
from model_models import PlatformRequest, PlatformResponse


OPENAI_MODEL_CATALOG = {
    "gpt-4o": {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": ["chat", "vision", "function_calling"],
        "max_context_tokens": 128000,
        "input_price_per_1m": 5.00,
        "output_price_per_1m": 15.00,
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": ["chat", "vision", "function_calling"],
        "max_context_tokens": 128000,
        "input_price_per_1m": 0.15,
        "output_price_per_1m": 0.60,
    },
    "gpt-4-turbo": {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": ["chat", "function_calling"],
        "max_context_tokens": 128000,
        "input_price_per_1m": 10.00,
        "output_price_per_1m": 30.00,
    },
    "o1": {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": ["chat", "reasoning"],
        "max_context_tokens": 200000,
        "input_price_per_1m": 15.00,
        "output_price_per_1m": 60.00,
    },
    "o1-mini": {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": ["chat", "reasoning"],
        "max_context_tokens": 128000,
        "input_price_per_1m": 3.00,
        "output_price_per_1m": 12.00,
    },
}


def list_available_models() -> Dict[str, Dict]:
    return dict(OPENAI_MODEL_CATALOG)


def resolve_model_resource(
    model_name: Optional[str] = None,
    capability: Optional[str] = None,
    min_context_tokens: Optional[int] = None,
    budget_per_1m_input: Optional[float] = None,
) -> Tuple[str, Dict]:
    candidates = dict(OPENAI_MODEL_CATALOG)

    if model_name:
        if model_name in candidates:
            return model_name, candidates[model_name]
        client = get_platform_client()
        try:
            models = client.client.models.list()
            for m in models.data:
                if m.id == model_name:
                    candidates[m.id] = {
                        "provider": "openai",
                        "api_hostname": "api.openai.com",
                        "capabilities": [],
                        "max_context_tokens": 0,
                        "input_price_per_1m": 0.0,
                        "output_price_per_1m": 0.0,
                    }
                    return m.id, candidates[m.id]
        except Exception:
            pass
        raise ValueError(f"Model '{model_name}' not found in OpenAI catalog")

    if capability:
        filtered = {
            k: v
            for k, v in candidates.items()
            if capability in v.get("capabilities", [])
        }
        if filtered:
            candidates = filtered

    if min_context_tokens:
        candidates = {
            k: v
            for k, v in candidates.items()
            if v.get("max_context_tokens", 0) >= min_context_tokens
        }

    if budget_per_1m_input:
        candidates = {
            k: v
            for k, v in candidates.items()
            if v.get("input_price_per_1m", float("inf")) <= budget_per_1m_input
        }

    if not candidates:
        return "gpt-4o-mini", OPENAI_MODEL_CATALOG["gpt-4o-mini"]

    best_model = min(
        candidates.items(), key=lambda x: x[1].get("input_price_per_1m", float("inf"))
    )
    return best_model[0], best_model[1]


def get_resource_details(model_id: str) -> Dict:
    if model_id in OPENAI_MODEL_CATALOG:
        return OPENAI_MODEL_CATALOG[model_id]
    return {
        "provider": "openai",
        "api_hostname": "api.openai.com",
        "capabilities": [],
        "max_context_tokens": 0,
        "input_price_per_1m": 0.0,
        "output_price_per_1m": 0.0,
    }


def invoke_model(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> PlatformResponse:
    resolved_model, _ = resolve_model_resource(model_name=model_id)

    request = PlatformRequest(
        model_id=resolved_model,
        messages=[],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    from model_models import normalize_messages

    request.messages = normalize_messages(prompt, system_prompt, conversation_history)

    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    response = client.chat_completion(request)
    return response
