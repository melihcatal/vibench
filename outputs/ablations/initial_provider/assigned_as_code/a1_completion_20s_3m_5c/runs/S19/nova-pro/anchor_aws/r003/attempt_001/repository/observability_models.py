from datetime import datetime, timezone

def normalize_metric_payload(payload):
    payload["start_time"] = datetime.fromtimestamp(payload["start_time"], timezone.utc)
    payload["end_time"] = datetime.fromtimestamp(payload["end_time"], timezone.utc)
    return payload

def parse_metric_response(response):
    points = [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response["Datapoints"]]
    return {"points": sorted(points, key=lambda p: p["timestamp"])}