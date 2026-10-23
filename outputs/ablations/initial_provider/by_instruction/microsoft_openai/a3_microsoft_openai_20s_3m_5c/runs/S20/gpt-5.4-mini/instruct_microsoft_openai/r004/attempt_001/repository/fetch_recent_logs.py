from observability_client import get_client, time_range


def fetch_recent_logs(field_name, field_value, hours=24):
    client = get_client()
    rng = time_range(hours)
    return client.responses.create(
        model="gpt-4.1-mini",
        input=str({"field_name": field_name, "field_value": field_value, **rng}),
    )
