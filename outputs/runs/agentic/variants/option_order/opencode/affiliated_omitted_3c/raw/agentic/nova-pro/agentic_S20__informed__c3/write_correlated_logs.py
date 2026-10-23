import os
from datadog import initialize, api

os.environ["DD_API_KEY"] = "your_datadog_api_key"
os.environ["DD_APP_KEY"] = "your_datadog_app_key"

options = {"api_key": os.getenv("DD_API_KEY"), "app_key": os.getenv("DD_APP_KEY")}
initialize(**options)

log_data_1 = {
    "host": "example.com",
    "message": "Correlated log event 1",
    "service": "example_service",
    "status": "INFO",
    "ddtags": "correlation_id:12345",
}
log_data_2 = {
    "host": "example.com",
    "message": "Correlated log event 2",
    "service": "example_service",
    "status": "INFO",
    "ddtags": "correlation_id:12345",
}

api.submit(series=[log_data_1])
api.submit(series=[log_data_2])
