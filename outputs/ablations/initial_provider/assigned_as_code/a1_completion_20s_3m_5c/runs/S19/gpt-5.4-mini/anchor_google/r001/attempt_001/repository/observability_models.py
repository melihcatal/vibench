def normalize_scalar_points(series):
    points = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return sorted(points, key=lambda p: p["timestamp"])


def summarize_points(points):
    if not points:
        return {"count": 0, "min": None, "max": None, "avg": None, "latest": None}
    values = [p["value"] for p in points]
    return {"count": len(values), "min": min(values), "max": max(values), "avg": sum(values) / len(values), "latest": points[-1]}


def compare_series(left_points, right_points):
    left_summary = summarize_points(left_points)
    right_summary = summarize_points(right_points)
    return {"left": left_summary, "right": right_summary, "delta_avg": (left_summary["avg"] or 0) - (right_summary["avg"] or 0)}
