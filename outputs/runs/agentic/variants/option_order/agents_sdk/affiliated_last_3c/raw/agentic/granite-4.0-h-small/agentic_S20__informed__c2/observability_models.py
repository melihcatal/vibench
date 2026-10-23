import dataclasses, datetime

@dataclasses.dataclass
class LogEvent:
    timestamp: int = dataclasses.field(default_factory=lambda: int(datetime.datetime.utcnow().timestamp() * 1000))
    message: str = ""
    severity: str = "INFO"
    correlation_id: str = ""

    def to_dict(self):
        return dataclasses.asdict(self)

@dataclasses.dataclass
class QueryFilter:
    start_time: int = None
    end_time: int = None
    severity: str = "ERROR"

    def as_dict(self):
        return dataclasses.asdict(self)

@dataclasses.dataclass
class FetchFilter:
    field: str = "level"
    value: str = "INFO"
    duration_minutes: int = 60

    def as_dict(self):
        return dataclasses.asdict(self)
