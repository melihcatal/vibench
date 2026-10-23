import boto3
from typing import Dict, Any
from observability_client import parse_iso_time, get_default_region
from query_metric_window import query_metric_window

def compare_metric_series(
    config1: Dict[str, Any],
    config2: Dict[str, Any],
    start_time: str,
    end_time: str,
    period: int = 300
) -> Dict[str, float]:
    data1 = query_metric_window(
        config1['namespace'], config1['metric_name'], start_time, end_time,
        dimensions=config1.get('dimensions'), period=period
    )
    data2 = query_metric_window(
        config2['namespace'], config2['metric_name'], start_time, end_time,
        dimensions=config2.get('dimensions'), period=period
    )
    avg1 = sum(dp['Average'] for dp in data1) / len(data1) if data1 else 0.0
    avg2 = sum(dp['Average'] for dp in data2) / len(data2) if data2 else 0.0
    return {
        'average1': avg1,
        'average2': avg2,
        'difference': avg1 - avg2,
        'ratio': avg1 / avg2 if avg2 != 0 else float('inf')
    }
