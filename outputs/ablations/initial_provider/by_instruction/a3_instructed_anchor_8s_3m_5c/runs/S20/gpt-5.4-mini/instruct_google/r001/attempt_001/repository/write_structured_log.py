from observability_client import write_structured_event


def main() -> None:
    write_structured_event('structured log event', severity='INFO', service='checkout', source='google-cloud-logging')


if __name__ == '__main__':
    main()
