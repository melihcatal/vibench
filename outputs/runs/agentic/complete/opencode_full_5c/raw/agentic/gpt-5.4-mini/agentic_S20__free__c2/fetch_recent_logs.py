from datetime import datetime, timedelta, timezone
from observability_client import create_client, log_index_name


def main() -> None:
    client = create_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    response = client.search(
        index=log_index_name(),
        body={
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "timestamp": {
                                    "gte": start.isoformat(),
                                    "lte": end.isoformat(),
                                }
                            }
                        },
                        {"term": {"service": "checkout-api"}},
                    ]
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 100,
        },
    )
    print(response)


if __name__ == "__main__":
    main()
