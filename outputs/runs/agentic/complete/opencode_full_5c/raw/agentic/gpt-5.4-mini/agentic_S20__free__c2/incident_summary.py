from collections import Counter
from observability_models import LogQueryResult


def summarize(result: LogQueryResult) -> str:
    severities = Counter(hit.get("severity", "UNKNOWN") for hit in result.hits)
    top = ", ".join(f"{k}:{v}" for k, v in severities.most_common())
    return f"total={result.total}; severities={top}"
