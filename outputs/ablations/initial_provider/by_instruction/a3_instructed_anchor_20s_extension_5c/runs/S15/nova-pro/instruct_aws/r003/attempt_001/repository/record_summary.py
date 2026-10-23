def summarize_records(records):
    summaries = []
    for record in records:
        summary = {
            'id': record['id'],
            'title': record['title'],
            'created_at': record['created_at']
        }
        summaries.append(summary)
    return summaries