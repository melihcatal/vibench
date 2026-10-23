import os
import requests


def get_datadog_base_url():
    return os.getenv("DD_SITE", "https://api.datadoghq.com")


def build_datadog_session():
    session = requests.Session()
    api_key = os.getenv("DD_API_KEY", "")
    app_key = os.getenv("DD_APP_KEY", "")
    session.headers.update({"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key, "Accept": "application/json"})
    return session
