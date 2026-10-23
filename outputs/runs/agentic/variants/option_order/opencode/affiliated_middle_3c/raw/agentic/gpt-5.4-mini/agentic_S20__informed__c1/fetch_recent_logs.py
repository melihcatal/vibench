from observability_client import fetch_recent_logs


def main() -> None:
    fetch_recent_logs(
        field_filters={"service": "checkout", "environment": "production"},
        time_from="now-15m",
        time_to="now",
        limit=50,
    )


if __name__ == "__main__":
    main()
