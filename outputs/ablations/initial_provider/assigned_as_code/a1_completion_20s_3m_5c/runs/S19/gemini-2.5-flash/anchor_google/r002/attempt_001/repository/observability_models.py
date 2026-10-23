from typing import List, Dict, Union


def normalize_time_series_points(timeseries_list: List[Dict]) -> List[Dict]:
    points = []
    for timeseries in timeseries_list:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return sorted(points, key=lambda p: p["timestamp"])

def format_time_interval(start_time: int, end_time: int) -> Dict[str, Dict[str, int]]:
    return {
        "start_time": {"seconds": start_time},
        "end_time": {"seconds": end_time}
    }
