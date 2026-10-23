from typing import List, Dict, Any, Optional
import json


def parse_metric_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return response.get("series", [])


def build_metric_query(
    metric_name: str,
    dimensions: Optional[Dict[str, str]] = None,
    aggregate: str = "avg",
) -> str:
    tags = [f"{k}:{v}" for k, v in (dimensions or {}).items()]
    tag_filter = ",".join(tags)
    if tag_filter:
        tag_filter = f"{{{tag_filter}}}"
    else:
        tag_filter = "{*}"
    return f"{aggregate}:{metric_name}{tag_filter}"


def extract_values_from_series(series_list: List[Dict[str, Any]]) -> List[float]:
    if not series_list:
        return []
    points = series_list[0].get("points", [])
    return [point[1] for point in points if len(point) > 1 and point[1] is not None]


def compute_stats(values: List[float]) -> Dict[str, float]:
    if not values:
        return {}
    return {
        "mean": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
        "count": len(values),
    }
