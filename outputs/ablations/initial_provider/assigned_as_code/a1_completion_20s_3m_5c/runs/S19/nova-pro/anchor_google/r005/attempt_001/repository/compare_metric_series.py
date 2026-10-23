import requests


def compare_metric_series(payload, config=None):
    config = config or {}
    url = f"https://management.azure.com/subscriptions/{config['subscription_id']}/resourceGroups/{config['resource_group']}/providers/Microsoft.Compute/virtualMachines/{config['vm_name']}/providers/microsoft.insights/metrics?api-version=2018-01-01"
    headers = {
        'Authorization': f'Bearer {config['access_token']}',
        'Content-Type': 'application/json'
    }
    data = {
        'timespan': f"{payload['start_time']}/{payload['end_time']}",
        'interval': 'PT1M',
        'metricnames': payload['metric_names'],
        'aggregation': 'Average'
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    series = response.json()['value']
    return {'series': series}