from observability_client import write_log_event


def main() -> None:
    write_log_event(
        {
            'service': 'checkout',
            'severity': 'info',
            'message': 'structured log event',
            'event_type': 'request.completed',
            'request_id': 'req_001',
        }
    )


if __name__ == '__main__':
    main()
