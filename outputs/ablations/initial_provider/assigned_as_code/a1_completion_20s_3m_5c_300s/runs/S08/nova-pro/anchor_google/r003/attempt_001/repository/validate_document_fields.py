from google.cloud import documentai


def validate_document_fields(response):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in response:
            raise ValueError(f"Missing required field: {field}")
    if response.get("confidence_score") < 0.5:
        raise ValueError("Confidence score is too low")
    return True