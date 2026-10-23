from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class TimeWindow:
    start: datetime
    end: datetime


@dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float
