from observability_client import query_logs


def main() -> None:
    query_logs(
        query="severity:ERROR",
        time_from="now-1h",
        time_to="now",
        filters={"service": "checkout"},
        limit=25,
    )


if __name__ == "__main__":
    main()
