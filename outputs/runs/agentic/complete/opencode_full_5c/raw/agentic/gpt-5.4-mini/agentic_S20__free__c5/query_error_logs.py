from observability_client import build_time_filter, query_entries


def main() -> list:
    filter_expr = build_time_filter(
        severity="ERROR",
        start_time="2026-04-20T00:00:00Z",
        end_time="2026-04-21T23:59:59Z",
        field_filters={"jsonPayload.service": "app-logs"},
    )
    return query_entries(filter_expr, limit=25)


if __name__ == "__main__":
    main()
