import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = os.getenv("MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model_family: str = DEFAULT_MODEL_FAMILY
    model_name: str = DEFAULT_MODEL_NAME


def load_model_config() -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        model_family=os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY),
        model_name=os.getenv("OPENAI_MODEL", DEFAULT_MODEL_NAME),
    )


def resolve_model_name(config: Optional[ModelConfig] = None, family: Optional[str] = None) -> str:
    cfg = config or load_model_config()
    target_family = family or cfg.model_family
    if target_family == "gpt-5":
        return cfg.model_name or "gpt-5.4-mini"
    if target_family == "gpt-4.1":
        return os.getenv("OPENAI_GPT41_MODEL", "gpt-4.1-mini")
    if target_family == "gpt-4o":
        return os.getenv("OPENAI_GPT4O_MODEL", "gpt-4o-mini")
    return cfg.model_name or DEFAULT_MODEL_NAME


def create_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_model_config()
    return OpenAI(
        api_key=cfg.api_key,
        base_url=cfg.base_url,
        organization=cfg.organization,
        project=cfg.project,
    )


def build_chat_messages(system: Optional[str], user: str, history: Optional[Iterable[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    if history:
        messages.extend(list(history))
    messages.append({"role": "user", "content": user})
    return messages


def complete_text(
    user: str,
    system: Optional[str] = None,
    history: Optional[Iterable[Dict[str, str]]] = None,
    model: Optional[str] = None,
    family: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1024,
    config: Optional[ModelConfig] = None,
) -> str:
    cfg = config or load_model_config()
    client = create_client(cfg)
    selected_model = model or resolve_model_name(cfg, family)
    response = client.responses.create(
        model=selected_model,
        input=build_chat_messages(system, user, history),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    return getattr(response, "output_text", "") or ""


def complete_json(
    user: str,
    schema: Dict[str, Any],
    system: Optional[str] = None,
    history: Optional[Iterable[Dict[str, str]]] = None,
    model: Optional[str] = None,
    family: Optional[str] = None,
    config: Optional[ModelConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_model_config()
    client = create_client(cfg)
    selected_model = model or resolve_model_name(cfg, family)
    response = client.responses.create(
        model=selected_model,
        input=build_chat_messages(system, user, history),
        text={"format": {"type": "json_schema", "name": "model_client_output", "schema": schema, "strict": True}},
    )
    text = getattr(response, "output_text", "") or "{}"
    return __import__("json").loads(text)
