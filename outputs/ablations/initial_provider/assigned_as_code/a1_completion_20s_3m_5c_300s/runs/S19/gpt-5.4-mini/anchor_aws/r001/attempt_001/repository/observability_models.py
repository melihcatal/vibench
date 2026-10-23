from dataclasses import dataclass


def normalize_points(points):
    normalized = []
    for point in points or []:
        timestamp = point.get("timestamp")
        value = point.get("value")
        if timestamp is None or value is None:
            continue
        normalized.append({"timestamp": float(timestamp), "value": float(value)})
    return sorted(normalized, key=lambda item: item["timestamp"])


def build_dimensions(dimensions):
    return [{"Name": str(name), "Value": str(value)} for name, value in (dimensions or {}).items()]


def summarize_series(points):
    series = normalize_points(points)
    values = [p["value"] for p in series]
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "average": None, "change": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "average": sum(values) / len(values),
        "change": values[-1] - values[0],
    }


@dataclass
class MetricResponse:
    points: list

    def as_dict(self):
        return {"points": normalize_points(self.points)}
