def summarize_records(records):
    return {'count': len(records), 'ids': [record['id'] for record in records]}
