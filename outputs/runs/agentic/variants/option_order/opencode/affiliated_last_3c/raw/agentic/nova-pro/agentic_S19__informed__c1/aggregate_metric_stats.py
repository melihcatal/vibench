import os

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

import requests


def aggregate_metric_stats(metric_name, start_time, end_time):
    url = f"https://api.datadoghq.com/api/v1/query"
    params = {"query": f"avg:{metric_name}{{*}}", "start": start_time, "end": end_time}
    headers = {"DD-API-KEY": DD_API_KEY, "DD-APPLICATION-KEY": DD_APP_KEY}
    response = requests.get(url, params=params, headers=headers)
    return response.json()
