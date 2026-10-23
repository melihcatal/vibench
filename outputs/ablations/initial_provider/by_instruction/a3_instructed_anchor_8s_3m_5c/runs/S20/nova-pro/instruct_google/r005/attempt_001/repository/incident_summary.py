import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('error_logs')

def summarize_incident(severity, start_time, end_time):
    filter_ = f'severity={severity} AND timestamp > "{start_time}" AND timestamp < "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    summary = {
        'total_errors': 0,
        'error_messages': []
    }
    for entry in entries:
        summary['total_errors'] += 1
        summary['error_messages'].append(entry.payload['message'])
    return summary

if __name__ == '__main__':
    incident_summary = summarize_incident('ERROR', '2026-09-18T00:00:00Z', '2026-09-19T00:00:00Z')
    print(incident_summary)