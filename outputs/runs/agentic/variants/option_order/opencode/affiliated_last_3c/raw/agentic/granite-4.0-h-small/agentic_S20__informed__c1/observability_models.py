from typing import Dict, List


class LogEvent(Dict[str, Any]):
    """Encapsulates a single log entry with required fields.

    Subclassing dict makes it easy to construct payloads that match the
    expectations of the various logging SDKs.
    """

    def __init__(
        self,
        *,
        timestamp: str,
        level: str,
        message: str,
        correlation_id: str = None,
        **extra,
    ):
        super().__init__(
            timestamp=timestamp,
            level=level,
            message=message,
            correlation_id=correlation_id,
            **extra,
        )

    # Helper to produce a plain dict suitable for Serializers
    def to_dict(self) -> Dict[str, Any]:
        return dict(self)


class LogFilter:
    """Simple container for query parameters used by fetch/retrieve helpers.

    Attributes:
        start_time (str): ISO 8601 start timestamp (inclusive).
        end_time (str): ISO 8601 end timestamp (inclusive).
        field_filter (Dict[str, Any]): Optional key/value pairs to match in log fields.
        limit (int): Maximum number of records to return.
    """

    def __init__(
        self,
        *,
        start_time: str = None,
        end_time: str = None,
        field_filter: Dict[str, Any] = None,
        limit: int = 100,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.field_filter = field_filter or {}
        self.limit = limit
