import boto3


def validate_document_fields(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    required = {"VENDOR_NAME", "TOTAL"}
    validated = []
    for document in response["ExpenseDocuments"]:
        summary = {f["Type"]["Text"]: f for f in document.get("SummaryFields", [])}
        missing = sorted(required - set(summary))
        confidence = min((f.get("Confidence", 0.0) for f in summary.values()), default=0.0)
        validated.append({"missing": missing, "confidence": confidence, "valid": not missing and confidence >= float(config.get("min_confidence", 0.0))})
    return {"validation": validated}
