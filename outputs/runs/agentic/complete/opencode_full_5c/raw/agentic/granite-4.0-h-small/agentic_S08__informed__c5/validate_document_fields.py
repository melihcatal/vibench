from document_models import NormalizedExpense


class ValidateDocumentFields:
    REQUIRED_FIELDS = {"vendor", "date", "total"}

    @staticmethod
    def validate(expense: NormalizedExpense) -> bool:
        # Ensure all required fields are present and confidence scores are acceptable
        for field in ValidateDocumentFields.REQUIRED_FIELDS:
            if not getattr(expense, field):
                return False
        # Add more sophisticated checks (e.g., confidence > 0.8) as needed
        return True
