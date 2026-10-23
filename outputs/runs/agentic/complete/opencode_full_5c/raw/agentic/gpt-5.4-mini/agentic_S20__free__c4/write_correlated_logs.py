from observability_client import ObservabilityClient


def main():
    client = ObservabilityClient()
    request_id = "req_789"
    client.write_event(
        {
            "message": "request started",
            "severity": "info",
            "service": "api",
            "request_id": request_id,
        }
    )
    return client.write_event(
        {
            "message": "request completed",
            "severity": "info",
            "service": "api",
            "request_id": request_id,
        }
    )
