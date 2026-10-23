from document_models import ValidationHelper


def validate_document_fields(extracted_data):
    validation_result = ValidationHelper.validate_fields(extracted_data)
    return validation_result
