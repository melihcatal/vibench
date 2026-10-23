def summarize_records(records):
    summary = {}
    for record in records:
        for key, value in record.items():
            if key not in summary:
                summary[key] = []
            summary[key].append(value)
    return summary