def normalize_point(point):
    kind = point.value._pb.WhichOneof("value")
    if kind not in ("double_value", "int64_value"):
        raise ValueError("Expected a scalar numeric metric")
    return {"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))}


def normalize_points(series):
    points = []
    for timeseries in series:
        for point in timeseries.points:
            points.append(normalize_point(point))
    return sorted(points, key=lambda p: p["timestamp"])


def build_interval(payload):
    return {"start_time": {"seconds": int(payload["start_time"])}, "end_time": {"seconds": int(payload["end_time"])} }
