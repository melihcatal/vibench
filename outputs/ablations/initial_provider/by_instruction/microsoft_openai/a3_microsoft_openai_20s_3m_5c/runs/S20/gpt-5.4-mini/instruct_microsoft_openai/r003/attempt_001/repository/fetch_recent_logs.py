from observability_client import query_logs


def main() -> None:
    query_logs({'field_values': {'service': 'checkout'}, 'time_range': 'last_60m'})


if __name__ == '__main__':
    main()
