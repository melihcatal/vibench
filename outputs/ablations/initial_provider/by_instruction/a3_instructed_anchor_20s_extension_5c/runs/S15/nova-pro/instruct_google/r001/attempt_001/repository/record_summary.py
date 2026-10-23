def summarize_records(records):
    summaries = []
    for record in records:
        summary = {k: v for k, v in record.items() if k in ['title', 'description']}
        summaries.append(summary)
    return summaries