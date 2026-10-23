import requests


def summarize_metric_trends(payload):
    response = requests.post('https://api.openweathermap.org/data/2.5/forecast', params=payload)
    response.raise_for_status()
    data = response.json()
    trends = {
        'summary': data['city']['name'],
        'temperature': data['list'][0]['main']['temp']
    }
    return trends