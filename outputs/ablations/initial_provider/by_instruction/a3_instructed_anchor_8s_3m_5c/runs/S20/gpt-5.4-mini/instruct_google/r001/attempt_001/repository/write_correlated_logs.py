from observability_client import write_structured_event


def main() -> None:
    request_id = 'req-12345'
    write_structured_event('request started', severity='INFO', request_id=request_id, phase='start', provider='google-cloud-logging')
    write_structured_event('request completed', severity='INFO', request_id=request_id, phase='end', provider='google-cloud-logging')


if __name__ == '__main__':
    main()
