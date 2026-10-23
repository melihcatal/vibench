import os

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

import requests


def compare_metric_series(metric_name, start_time, end_time, tags1, tags2):
    url = f"https://api.datadoghq.com/api/v1/query"
    params1 = {
        "query": f"avg:{metric_name}{{{tags1}}}",
        "start": start_time,
        "end": end_time,
    }
    params2 = {
        "query": f"avg:{metric_name}{{{tags2}}}",
        "start": start_time,
        "end": end_time,
    }
    headers = {"DD-API-KEY": DD_API_KEY, "DD-APPLICATION-KEY": DD_APP_KEY}
    response1 = requests.get(url, params=params1, headers=headers)
    response2 = requests.get(url, params=params2, headers=headers)
    return response1.json(), response2.json()
