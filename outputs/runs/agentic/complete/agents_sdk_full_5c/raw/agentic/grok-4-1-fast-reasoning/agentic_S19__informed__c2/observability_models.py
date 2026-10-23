from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class DataPoint:
    timestamp: datetime
    value: float

@dataclass
class MetricStats:
    mean: float
    max_val: float
    min_val: float
    count: int
