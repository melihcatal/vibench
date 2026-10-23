def summarize_records(records):
    return [record['summary'] for record in records if 'summary' in record]