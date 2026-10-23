def normalize_time_range(payload):
    return {"start_time": int(payload["start_time"]), "end_time": int(payload["end_time"]) }


def normalize_metric_query(payload):
    return {"metric": payload["metric"], "start_time": int(payload["start_time"]), "end_time": int(payload["end_time"]) }


def points_to_series(points):
    return sorted(points, key=lambda item: item["timestamp"])
