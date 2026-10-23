import os
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


def build_log_payload(
    message,
    level="info",
    service=None,
    env=None,
    hostname=None,
    ddsource=None,
    custom_attrs=None,
):
    payload = {
        "message": message,
        "ddsource": ddsource or "python",
        "hostname": hostname or os.uname().nodename,
        "service": service or DD_SERVICE,
        "ddtags": f"env:{env or DD_ENV}",
        "status": level,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if custom_attrs:
        payload.update(custom_attrs)
    return payload


def send_log_to_datadog(payload):
    response = requests.post(
        DD_LOGS_INTAKE_URL,
        headers=get_dd_headers(),
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    return response


def write_structured_log(
    message,
    level="info",
    service=None,
    env=None,
    hostname=None,
    ddsource=None,
    custom_attrs=None,
):
    payload = build_log_payload(
        message=message,
        level=level,
        service=service,
        env=env,
        hostname=hostname,
        ddsource=ddsource,
        custom_attrs=custom_attrs,
    )
    return send_log_to_datadog(payload)
