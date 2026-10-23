from observability_client import get_client, time_range


def query_error_logs(hours=24, severity="ERROR"):
    client = get_client()
    rng = time_range(hours)
    return client.responses.create(
        model="gpt-4.1-mini",
        input=str({"severity": severity, **rng, "query": "managed log query"}),
    )
