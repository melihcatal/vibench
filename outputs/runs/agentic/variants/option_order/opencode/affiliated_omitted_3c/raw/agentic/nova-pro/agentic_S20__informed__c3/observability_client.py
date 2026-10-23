import os
from datadog import initialize, api


def initialize_client():
    os.environ["DD_API_KEY"] = os.getenv("DD_API_KEY")
    os.environ["DD_APP_KEY"] = os.getenv("DD_APP_KEY")
    options = {"api_key": os.getenv("DD_API_KEY"), "app_key": os.getenv("DD_APP_KEY")}
    initialize(**options)


def submit_log(log_data):
    api.submit(series=[log_data])
