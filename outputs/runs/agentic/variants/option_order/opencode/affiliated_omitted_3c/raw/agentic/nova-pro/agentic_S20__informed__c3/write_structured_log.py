import os
from datadog import initialize, api

os.environ["DD_API_KEY"] = "your_datadog_api_key"
os.environ["DD_APP_KEY"] = "your_datadog_app_key"

options = {"api_key": os.getenv("DD_API_KEY"), "app_key": os.getenv("DD_APP_KEY")}
initialize(**options)

log_data = {
    "host": "example.com",
    "message": "Structured log event",
    "service": "example_service",
    "status": "INFO",
}

api.submit(series=[log_data])
