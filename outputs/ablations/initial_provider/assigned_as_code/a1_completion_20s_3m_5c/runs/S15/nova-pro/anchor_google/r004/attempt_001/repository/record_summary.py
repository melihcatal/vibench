def summarize_records(records):
    return {"count": len(records), "sample": records[:3] if records else []}