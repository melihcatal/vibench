from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class MetricConfig:
    namespace: str
    metric_name: str
    dimensions: Optional[List[Dict[str, str]]] = None

@dataclass
class TimeWindow:
    start_time: str
    end_time: str
