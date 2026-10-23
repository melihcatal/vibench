def normalize_points(points):
    ordered = sorted(points, key=lambda p: p["timestamp"])
    return [{"timestamp": float(point["timestamp"]), "value": float(point["value"])} for point in ordered]


def extract_scalar_value(point):
    kind = point.value._pb.WhichOneof("value")
    if kind not in ("double_value", "int64_value"):
        raise ValueError("Expected a scalar numeric metric")
    return float(getattr(point.value, kind))


def build_time_window(payload):
    return {
        "start_time": {"seconds": int(payload["start_time"])},
        "end_time": {"seconds": int(payload["end_time"])},
    }
