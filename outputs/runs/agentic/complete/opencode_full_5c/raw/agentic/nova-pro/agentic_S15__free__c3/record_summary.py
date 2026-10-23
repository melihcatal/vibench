import json


def summarize_records(records):
    summary = {"total": len(records)}
    return json.dumps(summary)
