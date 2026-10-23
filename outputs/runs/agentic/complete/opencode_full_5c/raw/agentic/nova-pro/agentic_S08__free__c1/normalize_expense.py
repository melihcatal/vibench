from document_models import NormalizationHelper


def normalize_expense(extracted_data):
    normalized_data = NormalizationHelper.normalize_expense(extracted_data)
    return normalized_data
