import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class SecretAuditEmbeddingConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = DEFAULT_EMBEDDING_MODEL

    @classmethod
    def from_env(cls) -> "SecretAuditEmbeddingConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID"),
            model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        )


def create_openai_client(config: Optional[SecretAuditEmbeddingConfig] = None) -> OpenAI:
    cfg = config or SecretAuditEmbeddingConfig.from_env()
    client_kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        client_kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        client_kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        client_kwargs["organization"] = cfg.organization
    if cfg.project:
        client_kwargs["project"] = cfg.project
    return OpenAI(**client_kwargs)


def _normalize_notes(notes: str) -> str:
    return " ".join(notes.split())


def embed_secret_audit_notes(notes: str, config: Optional[SecretAuditEmbeddingConfig] = None) -> List[float]:
    cfg = config or SecretAuditEmbeddingConfig.from_env()
    client = create_openai_client(cfg)
    response = client.embeddings.create(model=cfg.model, input=_normalize_notes(notes))
    return list(response.data[0].embedding)


def build_secret_audit_embedding_record(notes: str, secret_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, config: Optional[SecretAuditEmbeddingConfig] = None) -> Dict[str, Any]:
    embedding = embed_secret_audit_notes(notes, config=config)
    record: Dict[str, Any] = {"embedding": embedding, "model": (config or SecretAuditEmbeddingConfig.from_env()).model}
    if secret_id is not None:
        record["secret_id"] = secret_id
    if metadata is not None:
        record["metadata"] = metadata
    return record
