from translate_service import translate_text
from database_models import DocumentFetchResponse


class RecordTranslate:
    @staticmethod
    def translate(
        response: DocumentFetchResponse, target_lang: str = "es"
    ) -> DocumentFetchResponse:
        """Translate user‑facing text fields in a document to the target language.

        Uses an external translation service. Returns the modified document wrapped in a Response.
        """
        if not response.found:
            return response
        doc = response.document
        # Identify string fields to translate
        string_fields = {k: str(v) for k, v in doc.items() if isinstance(v, str)}
        if not string_fields:
            return response  # nothing to translate
        translated = translate_text(string_fields, target_lang)
        # Merge translations back, preserving non‑string fields
        for k, v in translated.items():
            doc[k] = v
        return DocumentFetchResponse(found=True, document=doc)
