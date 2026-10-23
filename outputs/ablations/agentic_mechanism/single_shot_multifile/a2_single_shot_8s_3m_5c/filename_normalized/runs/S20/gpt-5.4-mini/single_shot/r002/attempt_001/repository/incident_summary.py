import json
from collections import Counter
from observability_client import get_log_client, resolve_log_source
from observability_models import LogQuery, normalize_query_result


def main() -> dict:
    client = get_log_client()
    query = LogQuery(severity="ERROR", start_time="1970-01-01T00:00:00Z", end_time="2100-01-01T00:00:00Z", source=resolve_log_source("incident-summary"), limit=100)
    result = normalize_query_result(client.query_logs(query))
    messages = [item.get("payload", {}).get("message", "") for item in result["results"]]
    counts = Counter(messages)
    top_messages = [{"message": msg, "count": count} for msg, count in counts.most_common(5)]
    return {"error_count": result["count"], "top_messages": top_messages, "source": query.source}


if __name__ == "__main__":
    print(json.dumps(main()))
