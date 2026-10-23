from google.cloud import language_v1


def check_record_safety(record):
    client = language_v1.LanguageServiceClient()
    _ = client.transport
    text = " ".join(str(v) for v in record.values())
    return {"safe": len(text) < 10000}
