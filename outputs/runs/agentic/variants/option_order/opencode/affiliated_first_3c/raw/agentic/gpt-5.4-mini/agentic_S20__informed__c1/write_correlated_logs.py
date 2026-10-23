from observability_client import DatadogLogsClient, build_log_event


def write_correlated_logs() -> dict:
    client = DatadogLogsClient.from_env()
    request_id = "req_9b7c1a2f"
    events = [
        build_log_event(
            "request received",
            severity="INFO",
            fields={
                "service": "api",
                "request_id": request_id,
                "route": "/orders",
                "step": "received",
            },
        ),
        build_log_event(
            "payment processed",
            severity="INFO",
            fields={
                "service": "billing",
                "request_id": request_id,
                "route": "/orders",
                "step": "payment",
            },
        ),
        build_log_event(
            "request completed",
            severity="INFO",
            fields={
                "service": "api",
                "request_id": request_id,
                "route": "/orders",
                "step": "completed",
            },
        ),
    ]
    return {"results": client.write_events(events), "request_id": request_id}


if __name__ == "__main__":
    write_correlated_logs()
