import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelPlatformConfig:
    api_key: Optional[str]
    default_model: str
    organization: Optional[str]
    project: Optional[str]


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_platform_config() -> ModelPlatformConfig:
    return ModelPlatformConfig(
        api_key=_env("OPENAI_API_KEY"),
        default_model=_env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini",
        organization=_env("OPENAI_ORG_ID"),
        project=_env("OPENAI_PROJECT_ID"),
    )


def build_platform_client(config: Optional[ModelPlatformConfig] = None) -> OpenAI:
    cfg = config or load_platform_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.organization is not None:
        kwargs["organization"] = cfg.organization
    if cfg.project is not None:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def resolve_model_name(model: Optional[str] = None, config: Optional[ModelPlatformConfig] = None) -> str:
    cfg = config or load_platform_config()
    return (model or cfg.default_model).strip()


def get_platform_client(model: Optional[str] = None) -> tuple[OpenAI, str]:
    config = load_platform_config()
    return build_platform_client(config), resolve_model_name(model, config)
