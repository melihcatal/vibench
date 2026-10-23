def extract_points(result, aggregation_name):
    points = []
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                value = getattr(point, aggregation_name, None)
                if value is not None:
                    points.append({'timestamp': point.timestamp.timestamp(), 'value': float(value)})
    return sorted(points, key=lambda point: point['timestamp'])


def extract_series(result, aggregation_name):
    series = []
    for metric in result.metrics:
        for item in metric.timeseries:
            series.append({
                'dimensions': dict(item.metadata_values),
                'points': [
                    {'timestamp': point.timestamp.timestamp(), 'value': float(getattr(point, aggregation_name))}
                    for point in item.data if getattr(point, aggregation_name, None) is not None
                ],
            })
    return series
