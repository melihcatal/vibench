from safety_service import check_content_safety
from database_models import DocumentFetchResponse


class RecordTextSafety:
    @staticmethod
    def check(response: DocumentFetchResponse) -> bool:
        """Check user‑generated text fields in a document for unsafe content.

        Delegates to an external safety service. Returns True if safe, False otherwise.
        """
        if not response.found:
            return False  # nothing to check
        doc = response.document
        # Assume any string fields need moderation; collect them
        text_fields = [str(v) for v in doc.values() if isinstance(v, str)]
        if not text_fields:
            return True  # no text to moderate
        safe, _ = check_content_safety(text_fields)
        return safe
