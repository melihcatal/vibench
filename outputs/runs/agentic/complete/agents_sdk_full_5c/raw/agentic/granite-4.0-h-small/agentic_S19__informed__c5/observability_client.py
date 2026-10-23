import os
from google.cloud import monitoring_v3

class MonitoringClient:
    """Helper client for Google Cloud Monitoring (Stackdriver) Metrics API."""
    def __init__(self):
        # Credentials loaded from env var GOOGLE_APPLICATION_CREDENTIALS
        self.client = monitoring_v3.MetricServiceClient()
        self.project = os.getenv('GOOGLE_CLOUD_PROJECT') or self.client.project_path(os.getenv('GOOGLE_CLOUD_PROJECT'))

    def build_query(self, metric, window, filter_expr=None, aggregation=None):
        # Build a ListTimeSeriesRequest compatible query dict
        query = {
            'name': self.project,
            'filter': filter_expr or f"metric.type='{metric}'",
            'aggregation': aggregation or {},
            'interval': {
                'start_time': {'seconds': window['start_time'].timestamp()},
                'end_time': {'seconds': window['end_time'].timestamp()}
            }
        }
        return query

    def fetch_time_series(self, query):
        # ListTimeSeries returns a generator of Sample objects
        req = {
            'name': query['name'],
            'filter': query['filter'],
            'interval': query['interval']
        }
        if query.get('aggregation'):
            req['aggregation'] = query['aggregation']
        return list(self.client.list_time_series(request=req))

    def fetch_aggregated_stats(self, query):
        # Use the 'aggregation' field to request pre‑aggregated stats
        req = {
            'name': query['name'],
            'filter': query['filter'],
            'interval': query['interval']
        }
        if query.get('aggregation'):
            req['aggregation'] = query['aggregation']
        return list(self.client.query_time_series(request=req))

    def fetch_filtered_series(self, query):
        # Apply additional label filter on top of metric type
        req = {
            'name': query['name'],
            'filter': query.get('filter') or query.get('filter_expr') or '',
            'interval': query['interval']
        }
        return list(self.client.list_time_series(request=req))
