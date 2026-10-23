import os
from typing import Any, Dict, Optional

import requests

from observability_models import MetricQuery, normalize_points, normalize_tags, coerce_window

DD_API_BASE = os.getenv('DD_API_BASE', 'https://api.datadoghq.com')
DD_API_KEY = os.getenv('DD_API_KEY')
DD_APP_KEY = os.getenv('DD_APP_KEY')


class DatadogMetricsClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or DD_API_KEY
        self.app_key = app_key or DD_APP_KEY
        self.base_url = base_url or DD_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            'DD-API-KEY': self.api_key or '',
            'DD-APPLICATION-KEY': self.app_key or '',
            'Content-Type': 'application/json',
        })

    def _get(self, path: str, params: Dict[str, Any]):
        resp = self.session.get(self.base_url + path, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def query_metric(self, metric: str, start_time=None, end_time=None, filters=None, limit: int = 1000):
        start_time, end_time = coerce_window(start_time, end_time)
        query = MetricQuery(metric=metric, start_time=start_time, end_time=end_time, filters=filters or {}, limit=limit)
        data = self._get('/api/v1/query', query.to_params())
        series = data.get('series', []) if isinstance(data, dict) else []
        return {'metric': metric, 'series': normalize_points(series), 'raw': data}

    def get_aggregate_stats(self, metric: str, start_time=None, end_time=None, filters=None, aggregation: str = 'avg'):
        result = self.query_metric(metric, start_time, end_time, filters)
        values = []
        for series in result['series']:
            for point in series.get('pointlist', []) or []:
                if isinstance(point, (list, tuple)) and len(point) > 1 and point[1] is not None:
                    values.append(float(point[1]))
        if not values:
            return {'metric': metric, 'aggregation': aggregation, 'count': 0, 'value': None, 'raw': result['raw']}
        total = sum(values)
        stats = {'avg': total / len(values), 'sum': total, 'min': min(values), 'max': max(values), 'count': len(values)}
        return {'metric': metric, 'aggregation': aggregation, 'count': len(values), 'value': stats.get(aggregation, stats['avg']), 'stats': stats, 'raw': result['raw']}

    def filter_metric_dimensions(self, metric: str, dimensions: Dict[str, str], start_time=None, end_time=None):
        return self.query_metric(metric, start_time, end_time, normalize_tags(dimensions=dimensions))

    def compare_metric_series(self, metric: str, left: Dict[str, str], right: Dict[str, str], start_time=None, end_time=None):
        left_result = self.query_metric(metric, start_time, end_time, normalize_tags(left))
        right_result = self.query_metric(metric, start_time, end_time, normalize_tags(right))
        def mean(series_payload):
            vals = []
            for series in series_payload['series']:
                for point in series.get('pointlist', []) or []:
                    if isinstance(point, (list, tuple)) and len(point) > 1 and point[1] is not None:
                        vals.append(float(point[1]))
            return sum(vals) / len(vals) if vals else None
        return {'metric': metric, 'left': mean(left_result), 'right': mean(right_result), 'left_series': left_result['series'], 'right_series': right_result['series']}

