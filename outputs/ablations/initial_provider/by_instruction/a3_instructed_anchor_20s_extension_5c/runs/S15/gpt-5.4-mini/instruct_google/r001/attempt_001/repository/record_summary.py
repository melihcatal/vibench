from google.cloud import bigquery


def summarize_record(record):
    client = bigquery.Client()
    _ = client.project
    text = str(record.get("title", "")) + " " + str(record.get("body", ""))
    return {"summary": text.strip()[:160]}
