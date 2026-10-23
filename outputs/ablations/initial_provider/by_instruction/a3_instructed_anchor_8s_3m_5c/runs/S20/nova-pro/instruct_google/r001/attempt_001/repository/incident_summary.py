from google.cloud import logging

client = logging.Client()
log_name = 'error_logs'
logger = client.logger(log_name)

def summarize_incident(severity, start_time, end_time):
    filter_ = f'severity={severity} AND timestamp >= "{start_time}" AND timestamp <= "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    summary = {
        'total_errors': 0,
        'error_messages': []
    }
    for entry in entries:
        summary['total_errors'] += 1
        summary['error_messages'].append(entry.payload['message'])
    return summary

start_time = '2026-09-18T00:00:00Z'
end_time = '2026-09-19T00:00:00Z'

incident_summary = summarize_incident('ERROR', start_time, end_time)
print(incident_summary)