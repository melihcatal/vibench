from dataclasses import dataclass


def normalize_event(event, defaults=None):
    data = dict(defaults or {})
    data.update(event or {})
    return data


def normalize_time_range(start_time=None, end_time=None):
    return {"start_time": start_time, "end_time": end_time}


@dataclass
class LogQueryResult:
    entries: list
    next_page_token: str | None = None


@dataclass
class LogWriteResult:
    submitted: bool
    inserted_count: int = 1
