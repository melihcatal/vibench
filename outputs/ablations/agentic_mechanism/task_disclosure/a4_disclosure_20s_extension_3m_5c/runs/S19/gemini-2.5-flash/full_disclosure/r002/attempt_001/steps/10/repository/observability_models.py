import dataclasses
from datetime import datetime
from typing import Dict, Any, List, Optional

@dataclasses.dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Optional[Dict[str, str]] = None
    aggregation: Optional[str] = None

@dataclasses.dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float

@dataclasses.dataclass
class MetricQueryResponse:
    metric_name: str
    datapoints: List[MetricDatapoint]

# Normalization helper (placeholder, can be expanded based on specific needs)
def normalize_metric_data(raw_data: Any) -> MetricQueryResponse:
    # This is a placeholder for actual normalization logic
    # In a real scenario, this would parse raw API responses
    # and transform them into the MetricQueryResponse format.
    print(f"Normalizing raw data: {raw_data}") # For debugging purposes
    return MetricQueryResponse(metric_name="unknown", datapoints=[])
