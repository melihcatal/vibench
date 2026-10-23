from observability_client import LogQuery, query_log_entries


def main() -> None:
    query = LogQuery(project_id='google-cloud-project', filter_expression='severity>=ERROR AND timestamp >= "-P24H"', page_size=50)
    query_log_entries(query)


if __name__ == '__main__':
    main()
