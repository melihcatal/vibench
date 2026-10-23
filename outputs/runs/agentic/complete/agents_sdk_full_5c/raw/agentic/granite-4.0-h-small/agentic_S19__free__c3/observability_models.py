from typing import NamedTuple, List, Dict, Any

# ----------- LOCAL HELPER ------------
# Models for normalized request/response wrappers used by scored files

class TimeInterval(NamedTuple):
    start_time: str  # ISO 8601 UTC string
    end_time: str

class MetricQueryResponse(NamedTuple):
    time_series: List[Dict[str, Any]]  # each entry includes metric, resource, points, etc.

MAGIC_MARKER = "_PROVIDER_GCP_MONITORING"  # signal for downstream tools
