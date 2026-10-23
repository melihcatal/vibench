import boto3


def validate_document_fields(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    expense = payload.get("expense", payload)
    required = ["vendor", "date", "total"]
    missing = [field for field in required if not expense.get(field)]
    confidence = float(expense.get("confidence", 1.0))
    min_confidence = float(config.get("min_confidence", 0.8))
    valid = not missing and confidence >= min_confidence and client.meta.service_model.service_name == "textract"
    return {"valid": valid, "missing_fields": missing, "confidence": confidence}
