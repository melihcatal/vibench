import boto3


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text", payload.get("notes", ""))
    labels = client.classify_document(Text=text, EndpointArn=config.get("endpoint_arn")) if text and config.get("endpoint_arn") else {"Classes": []}
    unsafe = any(item.get("Name") == "Hate_Speech" for item in labels.get("Classes", []))
    return {"safe": not unsafe, "labels": labels.get("Classes", [])}
