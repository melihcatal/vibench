import os
from azure.identity import DefaultAzureCredential
from azure.monitor import MonitorManagementClient


class ObservabilityModels:
    """Local request, response, and normalization helpers for Azure Monitor Metrics.

    Provides simple data classes / type hints for:
    - Metric query request payloads (dict)
    - Metric query response wrappers (dict)
    - Normalized metric datapoint objects (namedtuple or dataclass)
    """

    from dataclasses import dataclass
    from typing import List, Any, Optional

    @dataclass
    class MetricDatapoint:
        timestamp: str  # ISO 8601 timestamp
        value: float
        # Optional fields returned by Azure (min, max, total, count, etc.) are omitted here for brevity

    @dataclass
    class MetricQueryResult:
        timeseries: List[
            Any
        ]  # Azure returns a list of timeseries objects; each contains a 'data' list of datapoints

    def __init__(self):
        self.client = None  # placeholder; not used directly, helpers are static

    @staticmethod
    def normalize_response(raw_response) -> List[MetricDatapoint]:
        """Convert Azure's nested response into a flat list of MetricDatapoint objects."""
        datapoints = []
        for series in raw_response[0].timeseries:
            for dp in series.data:
                datapoints.append(
                    ObservabilityModels.MetricDatapoint(
                        timestamp=dp.timestamp, value=float(dp.value)
                    )
                )
        return datapoints
