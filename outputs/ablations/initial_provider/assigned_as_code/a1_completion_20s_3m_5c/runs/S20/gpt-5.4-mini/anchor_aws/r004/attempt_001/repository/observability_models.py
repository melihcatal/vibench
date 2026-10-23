import json


def normalize_event(event):
    if isinstance(event, str):
        try:
            return json.loads(event)
        except json.JSONDecodeError:
            return {"message": event}
    return dict(event)


def normalize_result(response):
    return {
        "items": response.get("events", []),
        "next_token": response.get("nextForwardToken") or response.get("nextToken"),
    }


def build_time_range(start_ms=None, end_ms=None, lookback_ms=None):
    return {
        "start_ms": start_ms,
        "end_ms": end_ms,
        "lookback_ms": lookback_ms,
    }
