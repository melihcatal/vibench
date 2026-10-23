from observability_client import LogQuery, build_time_range_filter, query_log_entries


def main() -> None:
    filter_expression = build_time_range_filter(field_filters={'service': 'checkout', 'provider': 'google-cloud-logging'}, hours=12)
    query = LogQuery(project_id='google-cloud-project', filter_expression=filter_expression, page_size=100)
    query_log_entries(query)


if __name__ == '__main__':
    main()
