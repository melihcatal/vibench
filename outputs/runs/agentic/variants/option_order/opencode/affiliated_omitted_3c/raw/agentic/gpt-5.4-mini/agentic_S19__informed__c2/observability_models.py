from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: dict
    period: int


def normalize_time_window(start_time, end_time):
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    return start_time, end_time


def response_to_payload(response, query):
    return {'query': asdict(query), 'datapoints': response.get('Datapoints', []), 'label': response.get('Label')}


def compare_series_payload(left, right):
    return {'left': left, 'right': right}
