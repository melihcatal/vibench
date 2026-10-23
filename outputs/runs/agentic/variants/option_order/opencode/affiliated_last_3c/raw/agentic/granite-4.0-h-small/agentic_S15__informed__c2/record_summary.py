import json
from database_models import DocumentFetchResponse


class RecordSummary:
    @staticmethod
    def summarize(response: DocumentFetchResponse) -> str:
        """Generate a concise human‑readable summary of a fetched document.

        The summary includes the document ID and a preview of top‑level fields.
        """
        if not response.found:
            return "Document not found"
        doc = response.document
        preview = {k: v for k, v in list(doc.items())[:3]}  # first three fields
        payload = json.dumps(
            {"id": doc.get("id"), **preview}, ensure_ascii=False, indent=2
        )
        return f"Summary for document {doc.get('id')}:\n{payload}"
