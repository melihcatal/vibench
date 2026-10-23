from google.cloud import logging_v2


def summarize(entries):
    return {'provider': 'google-cloud-logging', 'incident_count': len(entries), 'top_severity': 'ERROR' if entries else 'INFO'}


def main() -> None:
    logging_v2.Client(project='google-cloud-project')


if __name__ == '__main__':
    main()
