import os
import uuid
import time
from datetime import datetime, timedelta
from observability_client import get_logging_client
from observability_models import CorrelatedLogBatch


def write_correlated_logs(
    service_name: str, correlation_id: str = None, log_events: list = None
) -> dict:
    """
    Write application log events that include a shared request or correlation identifier to Datadog.

    Args:
        service_name: Name of the service generating the logs
        correlation_id: Shared correlation ID for the request chain (generated if None)
        log_events: List of log events with level, message, and optional extra fields

    Returns:
        Dictionary with correlation_id and log count
    """
    try:
        import datadog_api_client
        from datadog_api_client import ApiClient, Configuration
        from datadog_api_client.v2.api.logs_api import LogsApi
        from datadog_api_client.v2.model.http_log import HTTPLog
        from datadog_api_client.v2.model.http_log_item import HTTPLogItem

        if correlation_id is None:
            correlation_id = str(uuid.uuid4())

        if log_events is None:
            log_events = [
                {"level": "INFO", "message": f"Request started for {service_name}"},
                {"level": "INFO", "message": f"Processing request in {service_name}"},
                {"level": "INFO", "message": f"Request completed for {service_name}"},
            ]

        config = Configuration()
        config.api_key["apiKeyAuth"] = os.environ.get("DD_API_KEY")
        config.api_key["appKeyAuth"] = os.environ.get("DD_APP_KEY")
        config.server_variables["site"] = os.environ.get("DD_SITE", "datadoghq.com")

        api_client = ApiClient(config)
        logs_api = LogsApi(api_client)

        log_items = []
        timestamp = int(time.time())

        for i, event in enumerate(log_events):
            log_item = HTTPLogItem(
                ddsource=service_name,
                ddtags=f"env:{os.environ.get('ENVIRONMENT', 'dev')},service:{service_name},correlation_id:{correlation_id}",
                hostname=os.environ.get("HOSTNAME", "localhost"),
                message=event["message"],
                service=service_name,
                status=event.get("level", "INFO").lower(),
                timestamp=timestamp + i,
                additional_properties={
                    "correlation_id": correlation_id,
                    "request_id": correlation_id,
                    "log_index": i,
                    "total_logs": len(log_events),
                    **event.get("extra_fields", {}),
                },
            )
            log_items.append(log_item)

        body = HTTPLog(log_items)

        response = logs_api.submit_log(body)

        print(
            f"Wrote {len(log_events)} correlated logs to Datadog with correlation_id: {correlation_id}"
        )

        return {
            "correlation_id": correlation_id,
            "log_count": len(log_events),
            "service": service_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        print(f"Failed to write correlated logs to Datadog: {e}")
        return {"correlation_id": correlation_id, "log_count": 0, "error": str(e)}
