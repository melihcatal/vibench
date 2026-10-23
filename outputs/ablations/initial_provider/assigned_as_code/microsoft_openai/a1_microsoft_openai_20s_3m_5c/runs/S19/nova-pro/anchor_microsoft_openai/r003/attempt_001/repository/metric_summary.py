from google.cloud import monitoring_v3


def summarize_metric_trends(payload):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{payload['project_id']}/metricDescriptors/{payload['metric_type']}'
    result = client.list_time_series(name, filter=payload['filter'], interval=payload['interval'])
    points = [{'timestamp': point.interval.end_time.seconds, 'value': point.value.double_value}
               for point in result]
    return {'points': sorted(points, key=lambda point: point['timestamp'])}