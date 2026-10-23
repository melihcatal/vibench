import os
from typing import Any, Dict

from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, DocumentField


class StructuredDocumentClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

    def extract(
        self, request: DocumentRequest, schema: Dict[str, Any]
    ) -> DocumentResponse:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Extract structured document fields as valid JSON matching the provided schema.",
                },
                {
                    "role": "user",
                    "content": f"Document type: {request.document_type}\nSchema: {schema}\nText: {request.document_text}",
                },
            ],
        )
        parsed = getattr(response, "output_text", "{}")
        return DocumentResponse(
            provider="openai",
            fields=[DocumentField(name="raw", value=parsed, confidence=1.0)],
            raw={"response_id": response.id},
        )
