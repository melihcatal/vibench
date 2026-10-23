import os
import uuid
from datetime import datetime, timezone

import requests

DD_SITE = os.getenv("DD_SITE", "datadoghq.com")
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
DD_SERVICE = os.getenv("DD_SERVICE", "default-service")
DD_ENV = os.getenv("DD_ENV", "production")
DD_LOGS_INTAKE_URL = f"https://http-intake.logs.{DD_SITE}/api/v2/logs"


def get_dd_headers():
    return {
        "DD-API-KEY": DD_API_KEY,
        "Content-Type": "application/json",
    }


def build_correlated_log_payload(
    message,
    correlation_id=None,
    level="info",
    service=None,
    env=None,
    hostname=None,
    ddsource=None,
    span_id=None,
    trace_id=None,
    custom_attrs=None,
):
    corr_id = correlation_id or str(uuid.uuid4())
    payload = {
        "message": message,
        "ddsource": ddsource or "python",
        "hostname": hostname or os.uname().nodename,
        "service": service or DD_SERVICE,
        "ddtags": f"env:{env or DD_ENV},correlation_id:{corr_id}",
        "status": level,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "correlation_id": corr_id,
        "span_id": span_id or uuid.uuid4().hex[:16],
        "trace_id": trace_id or uuid.uuid4().hex[:32],
    }
    if custom_attrs:
        payload.update(custom_attrs)
    return payload


def send_correlated_logs_to_datadog(payloads):
    body = "\n".join(requests.compat.json.dumps(p) for p in payloads)
    response = requests.post(
        DD_LOGS_INTAKE_URL,
        headers=get_dd_headers(),
        data=body,
        timeout=15,
    )
    response.raise_for_status()
    return response


def write_correlated_logs(
    messages,
    correlation_id=None,
    level="info",
    service=None,
    env=None,
    hostname=None,
    ddsource=None,
    span_id=None,
    trace_id=None,
    custom_attrs=None,
):
    if isinstance(messages, str):
        messages = [messages]

    payloads = []
    for msg in messages:
        payloads.append(
            build_correlated_log_payload(
                message=msg,
                correlation_id=correlation_id,
                level=level,
                service=service,
                env=env,
                hostname=hostname,
                ddsource=ddsource,
                span_id=span_id,
                trace_id=trace_id,
                custom_attrs=custom_attrs,
            )
        )
    return send_correlated_logs_to_datadog(payloads)
