import requests
import os
import json


def summarize_audit_events(events: list[dict]) -> dict:
    datadog_api_key = os.environ.get("DATADOG_API_KEY")
    datadog_app_key = os.environ.get("DATADOG_APP_KEY")
    datadog_site = os.environ.get("DATADOG_SITE", "us5.datadoghq.com") # Example site

    if not datadog_api_key or not datadog_app_key:
        raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY must be set in environment variables.")

    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": datadog_api_key,
        "DD-APPLICATION-KEY": datadog_app_key,
    }

    # In a real scenario, you'd send logs to Datadog and then query/summarize them.
    # For this example, we'll simulate sending and then a basic local summary.
    # Datadog Logs API endpoint example: https://docs.datadoghq.com/api/latest/logs/#send-logs
    # Let's just simulate sending the events as logs for now.
    log_payload = [
        {
            "ddsource": "federated-login-audit",
            "ddtags": "env:prod,service:identity",
            "hostname": "login-service",
            "message": json.dumps(event)
        }
        for event in events
    ]

    try:
        # Simulating sending logs to Datadog, normally this would be a real API call
        # response = requests.post(f"https://http-intake.logs.{datadog_site}/api/v2/logs", headers=headers, json=log_payload)
        # response.raise_for_status()
        # print(f"Successfully sent {len(events)} audit events to Datadog (simulated).")

        # For the purpose of summarization, we'll just count event types locally.
        summary = {
            "total_events": len(events),
            "successful_logins": sum(1 for e in events if e.get("event_type") == "login_success"),
            "failed_logins": sum(1 for e in events if e.get("event_type") == "login_failure"),
            "consent_granted": sum(1 for e in events if e.get("event_type") == "consent_granted"),
        }
        return summary

    except requests.exceptions.RequestException as e:
        print(f"Error sending events to Datadog (simulated): {e}")
        raise

