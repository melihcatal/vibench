from google.cloud import logging
import os


def validate_document_fields(
    document_data: dict, required_fields: list, min_confidence: float = 0.8
) -> bool:
    """
    Validates required structured fields and confidence scores, logging results to Google Cloud Logging.
    """
    logging_client = logging.Client()
    logger = logging_client.logger("document_validation_logger")

    is_valid = True
    missing_fields = []
    low_confidence_fields = []

    for field in required_fields:
        if (
            field not in document_data
            or document_data[field] is None
            or document_data[field] == ""
        ):
            missing_fields.append(field)
            is_valid = False
        # Assuming confidence scores are stored alongside the field values, or as a separate 'confidence' dict
        # For simplicity, let's assume `document_data` contains `field_name_confidence` for each field
        elif (
            f"{field}_confidence" in document_data
            and document_data[f"{field}_confidence"] < min_confidence
        ):
            low_confidence_fields.append(
                f"{field} (score: {document_data[f'{field}_confidence']})"
            )
            is_valid = False

    if not is_valid:
        log_message = {
            "message": "Document validation failed",
            "document_data": document_data,
            "missing_fields": missing_fields,
            "low_confidence_fields": low_confidence_fields,
        }
        logger.log_struct(log_message, severity="ERROR")
    else:
        logger.log_struct(
            {
                "message": "Document validation successful",
                "document_data": document_data,
            },
            severity="INFO",
        )

    return is_valid
