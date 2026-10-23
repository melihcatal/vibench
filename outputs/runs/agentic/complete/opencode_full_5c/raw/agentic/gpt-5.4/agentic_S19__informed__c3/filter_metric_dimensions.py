from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from query_metric_window import query_metric_window


def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: Optional[Dict[str, Any]] = None,
    period: int = 60,
    stat: str = "Average",
    unit: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    return query_metric_window(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        stat=stat,
        dimensions=dimension_filters,
        unit=unit,
        region_name=region_name,
    )
