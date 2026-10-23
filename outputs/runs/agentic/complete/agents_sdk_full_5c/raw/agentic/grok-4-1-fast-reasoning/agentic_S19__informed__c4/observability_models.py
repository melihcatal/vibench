from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

@dataclass
class MetricStat:
    metric_name: str
    namespace: str = 'AWS/EC2'
    dimensions: Optional[List[Dict[str, str]]] = None
    period: int = 300
    stat: str = 'Average'
    unit: Optional[str] = None

def build_metric_data_query(query_id: str, stat: MetricStat) -> Dict[str, Any]:
    """Build MetricDataQuery for CloudWatch GetMetricData."""
    metric = {
        'MetricName': stat.metric_name,
        'Namespace': stat.namespace
    }
    if stat.dimensions:
        metric['Dimensions'] = stat.dimensions
    metric_stat = {
        'Metric': metric,
        'Period': stat.period,
        'Stat': stat.stat
    }
    if stat.unit:
        metric_stat['Unit'] = stat.unit
    return {'Id': query_id, 'MetricStat': metric_stat}

def recent_time_window(minutes: int = 60) -> tuple[datetime, datetime]:
    """Return UTC start/end for recent time window."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    return start_time, end_time