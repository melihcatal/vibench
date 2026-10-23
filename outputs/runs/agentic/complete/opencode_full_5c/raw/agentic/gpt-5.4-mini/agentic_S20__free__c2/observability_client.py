import os
from dataclasses import dataclass
from typing import Optional

from opensearchpy import OpenSearch


@dataclass
class ObservabilityConfig:
    endpoint: str
    username: Optional[str]
    password: Optional[str]
    index_prefix: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        endpoint=os.getenv("OPENSEARCH_URL", "https://localhost:9200"),
        username=os.getenv("OPENSEARCH_USERNAME"),
        password=os.getenv("OPENSEARCH_PASSWORD"),
        index_prefix=os.getenv("OPENSEARCH_INDEX_PREFIX", "logs"),
    )


def create_client() -> OpenSearch:
    cfg = load_config()
    http_auth = (cfg.username, cfg.password) if cfg.username and cfg.password else None
    return OpenSearch(
        hosts=[cfg.endpoint],
        http_auth=http_auth,
        use_ssl=cfg.endpoint.startswith("https://"),
        verify_certs=False,
    )


def log_index_name() -> str:
    cfg = load_config()
    return f"{cfg.index_prefix}-*"
