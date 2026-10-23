from typing import Any, Dict, Optional

from observability_client import list_metric_series, load_observability_config


def filter_metric_dimensions(namespace: Optional[str] = None, metric_name: Optional[str] = None, dimensions: Optional[Dict[str, str]] = None, client: Optional[Any] = None):
    config = load_observability_config()
    return list_metric_series(namespace or config["namespace"], metric_name or config["metric_name"], dimensions=dimensions or {}, client=client)
