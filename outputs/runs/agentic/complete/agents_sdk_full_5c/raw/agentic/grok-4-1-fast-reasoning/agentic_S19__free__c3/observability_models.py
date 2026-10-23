from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class MetricDatapoint:
    timestamp: datetime
    average: Optional[float] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    sample_count: Optional[float] = None
    sum_: Optional[float] = None
    unit: Optional[str] = None

@dataclass
class MetricStats:
    average: float
    min_: float
    max_: float
    sum_: float
    count: int
    stddev: Optional[float] = None