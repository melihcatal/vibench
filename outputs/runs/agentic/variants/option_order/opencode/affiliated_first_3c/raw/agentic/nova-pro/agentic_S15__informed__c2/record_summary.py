import boto3


def summarize_records(records):
    summary = {}
    for record in records:
        for key, value in record.items():
            if key != "data":
                summary[key] = value
    return summary
