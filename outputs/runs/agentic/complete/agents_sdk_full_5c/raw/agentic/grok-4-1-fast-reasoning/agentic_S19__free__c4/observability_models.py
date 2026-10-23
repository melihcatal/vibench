from typing import List, Dict, Any, Optional
from datetime import datetime

def create_metric_data_query(
    query_id: str,
    metric_name: str,
    namespace: str = 'AWS/EC2',
    dimensions: Optional[List[Dict[str, str]]] = None,
    period: int = 300,
    stat: str = 'Average',
    unit: Optional[str] = None
) -> Dict[str, Any]:
    metric = {
        'MetricName': metric_name,
        'Namespace': namespace,
    }
    if dimensions:
        metric['Dimensions'] = dimensions
    metric_stat = {
        'Metric': metric,
        'Period': period,
        'Stat': stat,
    }
    if unit:
        metric_stat['Unit'] = unit
    return {
        'Id': query_id,
        'MetricStat': metric_stat
    }

def parse_datapoints(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    timestamps = result.get('Timestamps', [])
    values = result.get('Values', [])
    datapoints = []
    for ts, val in zip(timestamps, values):
        datapoints.append({
            'timestamp': ts.isoformat(),
            'value': float(val)
        })
    return datapoints