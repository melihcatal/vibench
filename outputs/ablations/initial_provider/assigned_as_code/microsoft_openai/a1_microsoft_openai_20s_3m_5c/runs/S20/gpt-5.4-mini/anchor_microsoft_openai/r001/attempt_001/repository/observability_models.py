from datetime import datetime, timezone


def iso_utc(dt):
    if dt is None:
        return None
    if isinstance(dt, (int, float)):
        return datetime.fromtimestamp(dt / 1000 if dt > 10**12 else dt, tz=timezone.utc).isoformat()
    if isinstance(dt, str):
        return dt
    return dt.astimezone(timezone.utc).isoformat()


def normalize_log_event(event):
    data = dict(event)
    for key in ('timestamp', 'time', 'TimeGenerated'):
        if key in data:
            data[key] = iso_utc(data[key])
    return data


def normalize_rows(rows):
    return [normalize_log_event(row) for row in rows]


def make_time_range(hours=1):
    end = datetime.now(timezone.utc)
    start = end.timestamp() - hours * 3600
    return iso_utc(start), iso_utc(end)
