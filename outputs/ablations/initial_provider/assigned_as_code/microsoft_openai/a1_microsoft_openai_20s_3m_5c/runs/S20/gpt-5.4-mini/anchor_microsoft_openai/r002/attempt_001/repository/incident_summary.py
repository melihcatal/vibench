from observability_models import extract_table_rows

from query_error_logs import query_error_logs


def incident_summary(payload, config=None):
    result = query_error_logs(payload, config=config)
    records = result['records']
    return {
        'incident_title': payload.get('incident_title', 'Log incident summary'),
        'error_count': len(records),
        'sample_messages': [row.get('Message') or row.get('message') for row in records[:5]],
    }
