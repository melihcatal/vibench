def summarize_records(records):
    summary = {
        "total_records": len(records),
        "sample_record": records[0] if records else None,
    }
    return summary
