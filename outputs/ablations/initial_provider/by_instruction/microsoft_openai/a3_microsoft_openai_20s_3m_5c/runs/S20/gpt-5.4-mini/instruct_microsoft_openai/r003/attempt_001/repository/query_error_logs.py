from observability_client import query_logs


def main() -> None:
    query_logs({'severity': 'ERROR', 'time_range': 'last_15m'})


if __name__ == '__main__':
    main()
