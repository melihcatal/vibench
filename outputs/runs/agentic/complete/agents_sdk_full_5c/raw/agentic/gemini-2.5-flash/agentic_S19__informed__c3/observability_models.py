import datetime
from typing import List, Dict, Any

class MetricDataPoint:
    """Represents a single data point for a CloudWatch metric."""
    def __init__(self, timestamp: datetime.datetime, value: float, unit: str = None):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit
        }

class MetricStatistics:
    """Represents aggregated statistics for a CloudWatch metric."""
    def __init__(self, timestamp: datetime.datetime, statistics: Dict[str, float], unit: str = None):
        self.timestamp = timestamp
        self.statistics = statistics
        self.unit = unit

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "statistics": self.statistics,
            "unit": self.unit
        }

class Dimension:
    """Represents a metric dimension for CloudWatch."""
    def __init__(self, name: str, value: str):
        self.Name = name
        self.Value = value

    def to_dict(self):
        return {"Name": self.Name, "Value": self.Value}

def parse_get_metric_statistics_response(response: Dict[str, Any]) -> List[MetricStatistics]:
    """Parses the response from CloudWatch get_metric_statistics."""
    parsed_data = []
    for dp in response.get('Datapoints', []):
        stats = {
            'SampleCount': dp.get('SampleCount'),
            'Average': dp.get('Average'),
            'Sum': dp.get('Sum'),
            'Minimum': dp.get('Minimum'),
            'Maximum': dp.get('Maximum'),
        }
        # Filter out None values
        stats = {k: v for k, v in stats.items() if v is not None}
        parsed_data.append(MetricStatistics(
            timestamp=dp.get('Timestamp'),
            statistics=stats,
            unit=dp.get('Unit')
        ))
    return parsed_data

def parse_get_metric_data_response(response: Dict[str, Any]) -> Dict[str, List[MetricDataPoint]]:
    """Parses the response from CloudWatch get_metric_data."""
    parsed_data = {}
    for result in response.get('MetricDataResults', []):
        id = result.get('Id')
        datapoints = []
        timestamps = result.get('Timestamps', [])
        values = result.get('Values', [])
        unit = result.get('Unit') # Unit is sometimes at the MetricDataResult level

        for i in range(len(timestamps)):
            datapoints.append(MetricDataPoint(
                timestamp=timestamps[i],
                value=values[i],
                unit=unit
            ))
        parsed_data[id] = datapoints
    return parsed_data

