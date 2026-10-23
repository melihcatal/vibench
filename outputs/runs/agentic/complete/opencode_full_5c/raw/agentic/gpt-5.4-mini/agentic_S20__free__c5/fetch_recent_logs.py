from observability_client import build_time_filter, query_entries


def main() -> list:
    filter_expr = build_time_filter(
        start_time="2026-04-21T00:00:00Z",
        field_filters={
            "jsonPayload.service": "app-logs",
            "jsonPayload.attributes.event_type": "structured",
        },
    )
    return query_entries(filter_expr, limit=50)


if __name__ == "__main__":
    main()
