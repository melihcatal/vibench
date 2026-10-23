import os

from datadog import initialize, api


def configure_client(api_key, app_key):
    options = {
        'api_key': api_key,
        'app_key': app_key
    }
    initialize(**options)


def query_logs(query, start, end):
    response = api.Log.search(
        query=query,
        start=start,
        end=end
    )
    return response


def ingest_log(message, source='python', service='example-service'):
    api.Log.send(
        message=message,
        source=source,
        service=service
    )