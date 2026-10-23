import os

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

import requests


def compare_metric_series(metric_name, resource1, resource2, start_time, end_time):
    url = f"https://api.datadoghq.com/api/v1/query"
    params = {
        "query": f"avg:{metric_name}{{*}}.by(host).rollup(sum, 60).group_by(host)",
        "start": start_time,
        "end": end_time,
    }
    headers = {"DD-API-KEY": DD_API_KEY, "DD-APPLICATION-KEY": DD_APP_KEY}
    response = requests.get(url, params=params, headers=headers)
    return response.json()
