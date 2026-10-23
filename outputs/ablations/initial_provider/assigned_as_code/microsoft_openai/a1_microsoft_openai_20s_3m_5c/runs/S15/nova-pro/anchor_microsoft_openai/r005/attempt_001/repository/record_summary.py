def summarize_record(record):
    summary = {}
    for key, value in record.items():
        if isinstance(value, str):
            summary[key] = value[:50] + '...' if len(value) > 50 else value
    return summary