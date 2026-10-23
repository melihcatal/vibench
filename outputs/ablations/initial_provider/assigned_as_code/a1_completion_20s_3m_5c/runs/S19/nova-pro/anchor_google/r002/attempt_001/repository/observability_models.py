import json

from google.cloud import monitoring_v3

def normalize_payload(payload):
    return {
        'metric': payload['metric'],
        'start_time': payload['start_time'],
        'end_time': payload['end_time'],
        'dimension': payload.get('dimension', None),
        'value': payload.get('value', None),
        'metric1': payload.get('metric1', None),
        'metric2': payload.get('metric2', None)
    }

def parse_response(response):
    return {
        'points': response['points'],
        'series1': response.get('series1', None),
        'series2': response.get('series2', None)
    }