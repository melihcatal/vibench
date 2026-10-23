from observability_client import get_client
from observability_models import LogQuery


def main() -> None:
    client = get_client()
    query = LogQuery(
        field_filters={"service": "checkout", "region": "us-east-1"},
        start_time="2026-04-22T00:00:00Z",
        end_time="2026-04-22T23:59:59Z",
        limit=20,
    )
    client.query_logs(query)


if __name__ == "__main__":
    main()
