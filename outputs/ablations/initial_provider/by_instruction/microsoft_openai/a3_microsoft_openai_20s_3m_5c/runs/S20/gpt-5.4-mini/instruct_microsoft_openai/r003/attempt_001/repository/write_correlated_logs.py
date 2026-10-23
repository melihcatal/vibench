from observability_client import write_log_event


def main() -> None:
    request_id = 'corr_001'
    write_log_event({'service': 'api', 'severity': 'info', 'message': 'start', 'request_id': request_id})
    write_log_event({'service': 'api', 'severity': 'info', 'message': 'finish', 'request_id': request_id})


if __name__ == '__main__':
    main()
